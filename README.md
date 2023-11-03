# MCS3-team17-bot_assistance

### Available Commands:

1. **HELLO**: Use this command to greet the application.

```
hello
```

2. **HELP**: If you need assistance, this command will provide you with helpful information.

```
help
```

3. **ADD**: Use this command to add an contact to your address book.

```
add @contact_name@ @contact_phone@
```

4. **ADD-BIRTHDAY**: This command is specifically for adding a birthday date.

```
add-birthday @contact_name@ @birthday_date@
```

5. **EDIT-BIRTHDAY**: Edit an birthday date using this command.

```
edit-birthday @contact_name@ @birthday_date@
```

6. **BIRTHDAYS**: View a list of upcoming birthdays for the next n days.

```
edit-birthday @contact_name@ @birthday_date@
```

7. **ADD-EMAIL**: Add an email address to a contact.

```
add-email @contact_name@ @email@
```

8. **EDIT-EMAIL**: Edit an email address for a contact.

```
edit-email @contact_name@ @email@
```

9. **ADD-ADDRESS**: Add an address for a contact.

```
add-address @contact_name@ @address@
```

10. **EDIT-ADDRESS**: Edit an address for a contact.

```
edit-email @contact_name@ @address@
```

11. **ADD-PHONE**: Add a extra phone number for a contact.

```
add-phone @contact_name@ @phone@
```

12. **EDIT-PHONE**: Edit an phone number for a contact.

```
edit-phone @contact_name@ @old_phone@ @new_phone@
```

13. **SHOW-CONTACTS**: View the list of all contacts with their info.

```
show-contacts
```

14. **SHOW-CONTACT**: View the info of a specific contact.

```
show-contact @contact_name@
```

15. **DELETE-CONTACT**: Remove a contact from the address book.

```
delete-contact @contact_name@
```

16. **ADD-NOTE**: Add a note(title, text, tags) to the notebook.

```
add-note @note_title@
```

17. **SHOW-NOTES**: View the list of all saved notes.

```
show-notes
```

18. **REMOVE-NOTE**: Delete a note from the notebook.

```
remove-note @note_title@
```

19. **GET-NOTE**: Retrieve the content of a specific note.

```
get-note @note_title@
```

20. **UPDATE-NOTE**: Modify the content(title, text, tags) of an existing note.

```
update-note @note_title@
```

21. **FIND-NOTES**: Search for notes based on search text.

```
find-notes @text@
```

22. **FIND-CONTACTS-BY-NAME**: Search for contacts by name.

```
find-contacts-by-name @search_text@
```

23. **FIND-CONTACTS-BY-PHONE**: Search for contacts by phone number.

```
find-contacts-by-phone @search_text@
```

24. **FIND-CONTACTS-BY-EMAIL**: Search for contacts by email address.

```
find-contacts-by-email @search_text@
```

25. **FIND-CONTACTS-BY-ADDRESS**: Search for contacts by address.

```
find-contacts-by-address @search_text@
```

26. **CLOSE**: Use this command to exit the bot.

```
close
```

27. **EXIT**: Use this command to exit the bot.

```
exit
```

28. **BYE**: Use this command to exit the bot.

```
bye
```

> Depending on your python version, run test.py file to run unit tests in specific >folder tests
> To run tests from root use something like:
> python3 -m unittest discover tests "test.py"
> To run tests from target folder tests use something like:
> python3 -m unittest test.py
