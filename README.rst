Introduction
============

This contains two dexterity behaviors, vocabularies and indexers for
two 'taxonomy-like' fields:

- ``classifiers_themes`` (e.g. `Air`, `Air > Quality`, `Air >
  Pollution`, `Water`)

- ``classifiers_categories`` (e.g. `Report`, `Project`, `Project
  > Management`)


Use case
========

You want to show some information on your website and make it easy to
find it.  You have reports about air or about water.  You also have
projects about those themes or specifically about air quality.  Some
projects are about both air and water.  Some reports are specifically
for management and some are more technical.

You want to be able to search all projects that are about the theme
air, whether this is about air in general or specifically about air
quality.  You also want to search on air quality in particular,
without finding the air pollution report.

How do you put this in a Plone Site?  A traditional way would be to
make two new content types: Report and Project.  You add a checkbox or
radio button to both types so you can mark them as technical or for
management.  You use the tags field to add an `air quality` tag or
other tags for the themes.

This can work, but it has a few downsides:

- You need two new content types, even though apart from the checkbox
  there is no difference between this and a standard page or maybe a
  folder.

- Not all tags are themes.  Editors may use tags for anything.  You
  may have an add-on or some custom code that already uses tags, for
  example to mark an item for showing up on the home page or in a
  collection.  So the theme tags get lost in the other tags.

Alternatively, instead of adding two new content types, you can use
tags to tag a standard page as a project or report and as technical or
for management.  This clutters up the tags even more.

To mark an item as a certain theme, you can also use a taxonomy, for
example `collective.taxonomy`_.  This is more flexible than this
package, but it may be overkill, trying to do too much.

Instead, ``collective.classifiers`` basically adds two fields, which
get their data from two dictionaries in the Plone configuration
registry.


Installation and usage
======================

Just add ``collective.classifiers`` to the eggs of your zope instance
in your buildout config, run buildout, and start the zope instance.
Go to the Plone Add-ons control panel of your website.  First activate
Dexterity content types if you have not done so already.  Then activate
``collective.classifiers``.

Go to the `Classifiers Settings` control panel, which simply accesses
the Plone configuration registry with a filter on
``collective.classifiers``.  You can edit the data there to create
categories and themes that fit your situation.  If editing does not
work because you get validation errors, please see the Dependencies_
section.

Let's say you add this data:

- Category `Report`, with sub categories `Management` and `Technical`.

- Category `Product`, with no sub categories except a white space
  character.  This is a trick to allow a top level category without
  any sub categories, as the top level may be enough.  The same trick
  can be done with themes.

- Theme `Air`, with sub themes `Quality` and `Pollution`.

- Theme `Water`, with sub themes `Rain` and `Rivers`.

Go to a type on the Dexterity types control panel, for example a Page.
Activate the categories classifiers and/or the themes classifiers
behavior.

You can now create or edit a Page and select multiple categories and
themes.  With the above data, you have these categories to choose from:

- Report

- Report > Management

- Report > Technical

- Product

You will have these themes:

- Air

- Air > Quality

- Air > Pollution

- Water

- Water > Rain

- Water > Rivers

Let's say you pick as category `Report > Management` and you pick
two themes: `Air` and `Water > Rain`.

The categories and themes are shown on the default view of the page,
but what is more interesting is that you can search for them in a
Collection.  In the edit form of a Collection you can select
Classifier Categories and Classifier Themes.  If you select as
category either `Report` or `Report > Management`, the page will
be found.  If you select as theme either `Air`, `Water` or `Water
> Rain`, the page will be found.


Dependencies
============

This is tested on Plone 4.3.2 with one version updated to a newer
release: plone.app.z3cform 0.7.5.  This should be the default in a
future Plone 4.3.3 release.  If you use an older plone.app.z3cform
release, editing the dictionaries through the web is not possible.
You would need to update the dictionaries by importing a
``registry.xml`` with your wanted settings then.  See
``collective/classifiers/profiles/testfixture/registry.xml`` for an
example.

Should work with Plone 4.2 as well, with the same remark about not
being able to edit the dictionaries through the web.


Sponsorship
===========

Work on collective.classifiers has been made possible by The Flemish
Environment Agency or VMM. See http://www.vmm.be . VMM operates as an agency of
the Flemish government for a better environment in Flanders. Flanders is one of
the three Belgian regions with its own government, parliament and
administration. The other two are the Brussels-Capital Region and the Walloon
Region.


.. _`collective.taxonomy`: https://pypi.python.org/pypi/collective.taxonomy
