# coding: utf8

'''Lifted from spacy.io's errors.py 
'''
from __future__ import unicode_literals

import os
import warnings
import inspect


def add_codes(err_cls):
    """Add error codes to string messages via class attribute names."""

    class ErrorsWithCodes(object):
        def __getattribute__(self, code):
            msg = getattr(err_cls, code)
            return "[{code}] {msg}".format(code=code, msg=msg)

    return ErrorsWithCodes()


# fmt: off

@add_codes
class Warnings(object):
    W001 = ("As of spaCy v2.0, the keyword argument `path=` is deprecated. "
            "You can now call spacy.load with the path as its first argument, "
            "and the model's meta.json will be used to determine the language "
            "to load. For example:\nnlp = spacy.load('{path}')")
    W002 = ("Tokenizer.from_list is now deprecated. Create a new Doc object "
            "instead and pass in the strings as the `words` keyword argument, "
            "for example:\nfrom spacy.tokens import Doc\n"
            "doc = Doc(nlp.vocab, words=[...])")
    W003 = ("Positional arguments to Doc.merge are deprecated. Instead, use "
            "the keyword arguments, for example tag=, lemma= or ent_type=.")
    W004 = ("No text fixing enabled. Run `pip install ftfy` to enable fixing "
            "using ftfy.fix_text if necessary.")
    W005 = ("Doc object not parsed. This means displaCy won't be able to "
            "generate a dependency visualization for it. Make sure the Doc "
            "was processed with a model that supports dependency parsing, and "
            "not just a language class like `English()`. For more info, see "
            "the docs:\nhttps://spacy.io/usage/models")
    W006 = ("No entities to visualize found in Doc object. If this is "
            "surprising to you, make sure the Doc was processed using a model "
            "that supports named entity recognition, and check the `doc.ents` "
            "property manually if necessary.")
    W007 = ("The model you're using has no word vectors loaded, so the result "
            "of the {obj}.similarity method will be based on the tagger, "
            "parser and NER, which may not give useful similarity judgements. "
            "This may happen if you're using one of the small models, e.g. "
            "`en_core_web_sm`, which don't ship with word vectors and only "
            "use context-sensitive tensors. You can always add your own word "
            "vectors, or use one of the larger models instead if available.")
    W008 = ("Evaluating {obj}.similarity based on empty vectors.")
    W009 = ("Custom factory '{name}' provided by entry points of another "
            "package overwrites built-in factory.")
    W010 = ("As of v2.1.0, the PhraseMatcher doesn't have a phrase length "
            "limit anymore, so the max_length argument is now deprecated.")
    W011 = ("It looks like you're calling displacy.serve from within a "
            "Jupyter notebook or a similar environment. This likely means "
            "you're already running a local web server, so there's no need to "
            "make displaCy start another one. Instead, you should be able to "
            "replace displacy.serve with displacy.render to show the "
            "visualization.")
    W012 = ("A Doc object you're adding to the PhraseMatcher for pattern "
            "'{key}' is parsed and/or tagged, but to match on '{attr}', you "
            "don't actually need this information. This means that creating "
            "the patterns is potentially much slower, because all pipeline "
            "components are applied. To only create tokenized Doc objects, "
            "try using `nlp.make_doc(text)` or process all texts as a stream "
            "using `list(nlp.tokenizer.pipe(all_texts))`.")
    W013 = ("As of v2.1.0, {obj}.merge is deprecated. Please use the more "
            "efficient and less error-prone Doc.retokenize context manager "
            "instead.")
    W014 = ("As of v2.1.0, the `disable` keyword argument on the serialization "
            "methods is and should be replaced with `exclude`. This makes it "
            "consistent with the other objects serializable.")
    W015 = ("As of v2.1.0, the use of keyword arguments to exclude fields from "
            "being serialized or deserialized is deprecated. Please use the "
            "`exclude` argument instead. For example: exclude=['{arg}'].")
    W016 = ("The keyword argument `n_threads` on the is now deprecated, as "
            "the v2.x models cannot release the global interpreter lock. "
            "Future versions may introduce a `n_process` argument for "
            "parallel inference via multiprocessing.")
    W017 = ("Alias '{alias}' already exists in the Knowledge base.")
    W018 = ("Entity '{entity}' already exists in the Knowledge base.")


@add_codes
class Errors(object):
    '''< 100: REST API related errors
       < 200: DB related errors
    '''
    E201 = ("Failed to connect to {db} instance")


@add_codes
class TempErrors(object):
    T003 = ("Resizing pre-trained Tagger models is not currently supported.")
    T004 = ("Currently parser depth is hard-coded to 1. Received: {value}.")
    T007 = ("Can't yet set {attr} from Span. Vote for this feature on the "
            "issue tracker: http://github.com/explosion/spaCy/issues")
    T008 = ("Bad configuration of Tagger. This is probably a bug within "
            "spaCy. We changed the name of an internal attribute for loading "
            "pre-trained vectors, and the class has been passed the old name "
            "(pretrained_dims) but not the new name (pretrained_vectors).")


# fmt: on


class MatchPatternError(ValueError):
    def __init__(self, key, errors):
        """Custom error for validating match patterns.

        key (unicode): The name of the matcher rule.
        errors (dict): Validation errors (sequence of strings) mapped to pattern
            ID, i.e. the index of the added pattern.
        """
        msg = "Invalid token patterns for matcher rule '{}'\n".format(key)
        for pattern_idx, error_msgs in errors.items():
            pattern_errors = "\n".join(["- {}".format(e) for e in error_msgs])
            msg += "\nPattern {}:\n{}\n".format(pattern_idx, pattern_errors)
        ValueError.__init__(self, msg)


class ModelsWarning(UserWarning):
    pass


WARNINGS = {
    "user": UserWarning,
    "deprecation": DeprecationWarning,
    "models": ModelsWarning,
}


def _get_warn_types(arg):
    if arg == "":  # don't show any warnings
        return []
    if not arg or arg == "all":  # show all available warnings
        return WARNINGS.keys()
    return [w_type.strip() for w_type in arg.split(",") if w_type.strip() in WARNINGS]


def _get_warn_excl(arg):
    if not arg:
        return []
    return [w_id.strip() for w_id in arg.split(",")]


SPACY_WARNING_FILTER = os.environ.get("SPACY_WARNING_FILTER")
SPACY_WARNING_TYPES = _get_warn_types(os.environ.get("SPACY_WARNING_TYPES"))
SPACY_WARNING_IGNORE = _get_warn_excl(os.environ.get("SPACY_WARNING_IGNORE"))


def user_warning(message):
    _warn(message, "user")


def deprecation_warning(message):
    _warn(message, "deprecation")


def models_warning(message):
    _warn(message, "models")


def _warn(message, warn_type="user"):
    """
    message (unicode): The message to display.
    category (Warning): The Warning to show.
    """
    if message.startswith("["):
        w_id = message.split("[", 1)[1].split("]", 1)[0]  # get ID from string
    else:
        w_id = None
    ignore_warning = w_id and w_id in SPACY_WARNING_IGNORE
    if warn_type in SPACY_WARNING_TYPES and not ignore_warning:
        category = WARNINGS[warn_type]
        stack = inspect.stack()[-1]
        with warnings.catch_warnings():
            if SPACY_WARNING_FILTER:
                warnings.simplefilter(SPACY_WARNING_FILTER, category)
            warnings.warn_explicit(message, category, stack[1], stack[2])
