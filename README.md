# Mini-Mart-Supermarket
order product from the online vendor
# Fixing Django Wishlist Migration and Database Mismatch

## Problem

While opening the Django admin wishlist page, the application returned:

```text
django.db.utils.OperationalError:
no such column: store_wishlist.user_id
```

The problem happened because the Django `WishList` model expected a `user_id` column, but the existing SQLite `store_wishlist` table did not contain it.

The database contained an older wishlist structure.

The existing table contained:

```text
id
date_created
date_updated
product_id
```

But the current `WishList` model contained:

```python
class WishList(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
```

Therefore, Django expected:

```text
id
user_id
date_created
date_updated
```

The database and Django migration state were out of sync.

## Cause

Migration `0007_wishlist_wishlistitem` was marked as applied using:

```text
python manage.py migrate store 0007 --fake
```

The `--fake` option updated Django's migration history without applying the database changes.

The migration history showed:

```text
[X] 0006_remove_product_user_wishlist
[ ] 0007_wishlist_wishlistitem
```

At an earlier stage, the wishlist tables already existed in SQLite, so Django attempted to create tables that were already present.

After using `--fake`, Django believed the migration had been applied, while the database still had the old table structure.

## Solution

### 1. Check the existing database table

Open the Django shell:

```text
python manage.py shell
```

Then inspect the wishlist table:

```python
from django.db import connection

cursor = connection.cursor()

cursor.execute("PRAGMA table_info(store_wishlist)")

print(cursor.fetchall())
```

The old table returned:

```text
[
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'date_created', 'datetime', 1, None, 0),
    (2, 'date_updated', 'date', 1, None, 0),
    (3, 'product_id', 'bigint', 1, None, 0)
]
```

This confirmed that `user_id` was missing.

It also showed an old `product_id` field inside `store_wishlist`.

## 2. Remove the old wishlist tables

Because the wishlist feature was still under development, the old wishlist tables were removed.

Inside the Django shell:

```python
cursor.execute("DROP TABLE IF EXISTS store_wishlistitem")

cursor.execute("DROP TABLE IF EXISTS store_wishlist")

connection.commit()
```

Then exit:

```python
exit()
```

This approach was used because the SQLite command-line program was not installed on Windows, so:

```text
python manage.py dbshell
```

returned:

```text
CommandError:
You appear not to have the 'sqlite3' program installed or on your path.
```

Django's database connection still provided access to the SQLite database.

## 3. Delete the incorrect wishlist migration

Delete only:

```text
store/migrations/0007_wishlist_wishlistitem.py
```

Do not delete migrations `0001` through `0006`.

## 4. Create a fresh migration

Run:

```text
python manage.py makemigrations store
```

Django should create:

```text
store/migrations/0007_wishlist_wishlistitem.py
```

with the current `WishList` and `WishListItem` models.

## 5. Apply the migration normally

Run:

```text
python manage.py migrate
```

Do not use:

```text
--fake
```

The migration should finish with:

```text
Applying store.0007_wishlist_wishlistitem... OK
```

## 6. Verify the migration

Run:

```text
python manage.py showmigrations store
```

The result should show:

```text
[X] 0001_initial
[X] 0002_rename_modifield_product_modifield_date
[X] 0003_alter_variation_time_added
[X] 0004_alter_variation_variation_value
[X] 0005_product_user_wishlist
[X] 0006_remove_product_user_wishlist
[X] 0007_wishlist_wishlistitem
```

## Wishlist Structure

The final wishlist structure is:

```text
CustomUser
    |
    | OneToOne
    ↓
WishList
    |
    | ForeignKey
    ↓
WishListItem
    |
    | ForeignKey
    ↓
Product
```

This means one user has one wishlist.

The wishlist contains multiple wishlist items.

Each wishlist item points to one product.

The current models are:

```python
class WishList(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
```

```python
class WishListItem(models.Model):
    wishlist = models.ForeignKey(
        WishList,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'product')
```

The `unique_together` constraint prevents the same product from being added to the same wishlist more than once.

## Key Lesson

Django migrations have two separate parts:

```text
Migration history
        +
Database schema
```

Both need to remain synchronized.

Using:

```text
python manage.py migrate --fake
```

only changes Django's migration history. It does not change the database structure.

Use `--fake` only when the database already has the exact schema represented by the migration.

When a new model creates new database tables during development, allow Django to execute the migration normally:

```text
python manage.py makemigrations
python manage.py migrate
```