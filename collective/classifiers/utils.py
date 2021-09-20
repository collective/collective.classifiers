SPLITTER = " > "
import six


def join_classifiers_terms(main, sub):
    if not isinstance(main, six.string_types):
        main = str(main)
    if not isinstance(sub, six.string_types):
        sub = str(sub)
    main = main.strip()
    sub = sub.strip()
    # Handle any existing occurences of the splitter.  We can remove
    # it, replace it, or raise an error.
    main = main.replace(SPLITTER, " SPLITTER ")
    sub = sub.replace(SPLITTER, " SPLITTER ")
    # One of the terms might be empty, especially after stripping
    # spaces.
    return SPLITTER.join([term for term in (main, sub) if term])


def split_classifiers_term(term):
    # Split term into main and sub theme.
    return term.split(SPLITTER, 1)


def extract_all_classifiers(classifiers):
    """Extract main and sub classifiers from list of classifiers.
    From ['main > sub 1', 'main > sub 2'] we extract:

      ['main', 'main > sub 1', 'main > sub 2']
    """
    result = set()
    for term in classifiers:
        result.add(split_classifiers_term(term)[0])
    result.update(classifiers)
    return sorted(list(result))


def extract_sub_classifiers(classifiers):
    """Extract sub classifiers from list of classifiers.
    From ['main > sub 1', 'main > sub 2'] we extract:

      ['main > sub 1', 'main > sub 2']

    Only if 'main' is in the list on its own, do we return that one
    as well.
    """
    result = set()
    result.update(classifiers)
    return sorted(list(result))
