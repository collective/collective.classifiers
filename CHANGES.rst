Changelog
=========

0.4.1 (2014-04-07)
------------------

- Nothing changed yet.


0.4 (2014-03-05)
----------------

- Add upgrade step to fix the values currently in the catalog.
  [maurits]

- Do not let themes and categories end up in the catalog index when
  the behavior is not activated for a portal_type.
  [maurits]


0.3 (2014-02-24)
----------------

- Handle case where values is None.
  [maurits]


0.2 (2014-02-24)
----------------

- Make values not required.  Until now you could fake an empty values
  list by typing a space as value.  In some circumstances, next time
  you edited the configuration, you would need to do this again
  because the space was stripped.
  [maurits]


0.1 (2013-11-09)
----------------

- Initial release
