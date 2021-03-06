# coding: utf-8

from unittest import TestCase

from django.template import Context, Variable, VariableDoesNotExist


class ContextTests(TestCase):
    def test_context(self):
        c = Context({"a": 1, "b": "xyzzy"})
        self.assertEqual(c["a"], 1)
        self.assertEqual(c.push(), {})
        c["a"] = 2
        self.assertEqual(c["a"], 2)
        self.assertEqual(c.get("a"), 2)
        self.assertEqual(c.pop(), {"a": 2})
        self.assertEqual(c["a"], 1)
        self.assertEqual(c.get("foo", 42), 42)

        with c.push():
            c['a'] = 2
            self.assertEqual(c['a'], 2)
        self.assertEqual(c['a'], 1)

        with c.push(a=3):
            self.assertEqual(c['a'], 3)
        self.assertEqual(c['a'], 1)

    def test_resolve_on_context_method(self):
        # Regression test for #17778
        empty_context = Context()
        self.assertRaises(VariableDoesNotExist,
                Variable('no_such_variable').resolve, empty_context)
        self.assertRaises(VariableDoesNotExist,
                Variable('new').resolve, empty_context)
        self.assertEqual(Variable('new').resolve(Context({'new': 'foo'})), 'foo')
