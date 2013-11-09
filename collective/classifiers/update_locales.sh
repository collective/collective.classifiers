#! /bin/sh
# our domain
i18ndude rebuild-pot --pot locales/collective.classifiers.pot --merge locales/manual.pot .
for po in locales/*/LC_MESSAGES/collective.classifiers.po; do
    i18ndude sync --pot locales/collective.classifiers.pot $po
done

# plone domain
i18ndude rebuild-pot --pot locales/plone.pot --create plone profiles/
for po in locales/*/LC_MESSAGES/plone.po; do
    i18ndude sync --pot locales/plone.pot $po
done
