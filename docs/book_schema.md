### The Book Schema

At the moment, the company is manually uploading the books to their database. The database has the following schema about the books that is stored in the Mongo database:

1. Title
2. Author
3. Description
4. Language
5. Publisher
6. Published Date
7. ISBN
8. Price
9. Status (PENDING, ACTIVE, INACTIVE)
10. Created Date
11. Updated Date
12. Inactive Date
13. Cover Images (URLs)
14. Genres (Array of Strings)
15. Book format (e.g., Paperback, Hardcover, eBook)
16. Ratings By Stars (Array of Objects with keys as stars and values as number of ratings, e.g., {1: 10, 2: 20, 3: 30, 4: 40, 5: 50})
17. Number Of Reviews
