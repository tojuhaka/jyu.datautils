from five import grok
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.component import queryUtility
from jyu.tutka.page.utilities import ITutkaUtility
from z3c.formwidget.query.interfaces import IQuerySource
from zope.schema.interfaces import IContextSourceBinder

class TutkaQueryHelper(object):
    def __contains__(self, term):
        return self.vocab.__contains__(term)

    def __iter__(self):
        return self.vocab.__iter__()

    def __len__(self):
        return self.vocab.__len__()

    def getTerm(self, value):
        return self.vocab.getTerm(value)

    def getTermByToken(self, value):
        return self.vocab.getTermByToken(value)


    def createVocabularyTerms(self, values):
        terms = []
        for v in values:
            try:
                token = value = v[0]
                title = v[1]
                terms.append(SimpleVocabulary.createTerm(value, token, title))
            except IndexError:
                pass
        return SimpleVocabulary(terms)

class SourceBinder(TutkaQueryHelper):
    grok.implements(IQuerySource)



