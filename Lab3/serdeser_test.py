import unittest
import serdeser


SerDeser = serdeser.Serdeser()
SerDeserXML = serdeser.Serdeser("xml")


class MyClass:
    class_variable = "class_variable"

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def method(self, c):
        return self.a + self.b + c

    @staticmethod
    def static_method(d):
        return d

    @classmethod
    def class_method(cls, e):
        return cls.class_variable + e


class MySubclass(MyClass):
    def method(self, c):
        return 2 * self.a + 2 * self.b + c


class ClassSerDeser(unittest.TestCase):
    def test_class_serialization(self):
        my_class = MyClass(1, 2)
        deserialized = SerDeser.deserialize(SerDeser.serialize(my_class))
        deserialized_xml = SerDeserXML.deserialize(SerDeserXML.serialize(my_class))
        self.assertIsInstance(deserialized, MyClass)
        self.assertEqual(deserialized.a, 1)
        self.assertEqual(deserialized.b, 2)
        self.assertIsInstance(deserialized_xml, MyClass)
        self.assertEqual(deserialized_xml.a, 1)
        self.assertEqual(deserialized_xml.b, 2)

    def test_subclass_serialization(self):
        my_subclass = MySubclass(1, 2)
        deserialized = SerDeser.deserialize(SerDeser.serialize(my_subclass))
        deserialized_xml = SerDeserXML.deserialize(SerDeserXML.serialize(my_subclass))
        self.assertIsInstance(deserialized, MySubclass)
        self.assertEqual(deserialized.a, 1)
        self.assertEqual(deserialized.b, 2)
        self.assertIsInstance(deserialized_xml, MySubclass)
        self.assertEqual(deserialized_xml.a, 1)
        self.assertEqual(deserialized_xml.b, 2)

    def test_static_method_serialization(self):
        my_class = MyClass(1, 2)
        self.assertIs(
            SerDeser.deserialize(SerDeser.serialize(my_class.static_method)),
            MyClass.static_method,
        )
        self.assertIs(
            SerDeserXML.deserialize(SerDeserXML.serialize(my_class.static_method)),
            MyClass.static_method,
        )

    def test_class_method_serialization(self):
        my_class = MyClass(1, 2)
        self.assertIs(
            SerDeser.deserialize(SerDeser.serialize(my_class.class_method)),
            MyClass.class_method,
        )
        self.assertIs(
            SerDeserXML.deserialize(SerDeserXML.serialize(my_class.class_method)),
            MyClass.class_method,
        )

    def test_builtin_scope_serialization(self):
        self.assertIs(SerDeser.deserialize(SerDeser.serialize(len)), len)
        self.assertIs(SerDeserXML.deserialize(SerDeserXML.serialize(len)), len)

    def test_global_scope_serialization(self):
        global_var = "global_var"
        self.assertEqual(
            SerDeser.deserialize(SerDeser.serialize(global_var)), global_var
        )
        self.assertEqual(
            SerDeserXML.deserialize(SerDeserXML.serialize(global_var)), global_var
        )

    def test_nonlocal_scope_serialization(self):
        def outer_func():
            nonlocal_var = "nonlocal_var"

            def inner_func():
                self.assertEqual(
                    SerDeser.deserialize(SerDeser.serialize(nonlocal_var)), nonlocal_var
                )
                self.assertEqual(
                    SerDeserXML.deserialize(SerDeserXML.serialize(nonlocal_var)),
                    nonlocal_var,
                )

            inner_func()

        outer_func()

    def test_local_scope_serialization(self):
        def func():
            local_var = "local_var"
            self.assertEqual(
                SerDeser.deserialize(SerDeser.serialize(local_var)), local_var
            )
            self.assertEqual(
                SerDeserXML.deserialize(SerDeserXML.serialize(local_var)), local_var
            )

        func()


class BasicSerDeSer(unittest.TestCase):
    def test_int(self):
        self.assertEqual(SerDeser.deserialize(SerDeser.serialize(42)), 42)
        self.assertEqual(SerDeserXML.deserialize(SerDeserXML.serialize(42)), 42)

    def test_float(self):
        self.assertAlmostEqual(SerDeser.deserialize(SerDeser.serialize(3.14)), 3.14)
        self.assertAlmostEqual(
            SerDeserXML.deserialize(SerDeserXML.serialize(3.14)), 3.14
        )

    def test_bool(self):
        self.assertEqual(SerDeser.deserialize(SerDeser.serialize(True)), True)
        self.assertEqual(SerDeserXML.deserialize(SerDeserXML.serialize(True)), True)

    def test_str(self):
        self.assertEqual(SerDeser.deserialize(SerDeser.serialize("hello")), "hello")
        self.assertEqual(
            SerDeserXML.deserialize(SerDeserXML.serialize("hello")), "hello"
        )

    def test_none(self):
        self.assertEqual(SerDeser.deserialize(SerDeser.serialize(None)), None)
        self.assertEqual(SerDeserXML.deserialize(SerDeserXML.serialize(None)), None)

    def test_tuple(self):
        self.assertEqual(SerDeser.deserialize(SerDeser.serialize((1, 2, 3))), (1, 2, 3))
        self.assertEqual(
            SerDeserXML.deserialize(SerDeserXML.serialize((1, 2, 3))), (1, 2, 3)
        )

    def test_list(self):
        self.assertEqual(SerDeser.deserialize(SerDeser.serialize([1, 2, 3])), [1, 2, 3])
        self.assertEqual(
            SerDeserXML.deserialize(SerDeserXML.serialize([1, 2, 3])), [1, 2, 3]
        )

    def test_set(self):
        self.assertEqual(SerDeser.deserialize(SerDeser.serialize({1, 2, 3})), {1, 2, 3})
        self.assertEqual(
            SerDeserXML.deserialize(SerDeserXML.serialize({1, 2, 3})), {1, 2, 3}
        )

    def test_dict(self):
        self.assertEqual(
            SerDeser.deserialize(SerDeser.serialize({"a": 1, "b": 2})), {"a": 1, "b": 2}
        )
        self.assertEqual(
            SerDeserXML.deserialize(SerDeserXML.serialize({"a": 1, "b": 2})),
            {"a": 1, "b": 2},
        )

    def test_lambda(self):
        f = lambda x: x * 2
        self.assertEqual(SerDeser.deserialize(SerDeser.serialize(f(3))), 6)
        self.assertEqual(SerDeserXML.deserialize(SerDeserXML.serialize(f(3))), 6)

    def test_closure(self):
        def outer():
            x = 10

            def inner():
                return x

            return inner

        inner_func = outer()
        self.assertEqual(SerDeser.deserialize(SerDeser.serialize(inner_func())), 10)
        self.assertEqual(
            SerDeserXML.deserialize(SerDeserXML.serialize(inner_func())), 10
        )

    def test_generator(self):
        def my_gen():
            for i in range(3):
                yield i

        gen_obj = my_gen()
        self.assertEqual(
            list(SerDeser.deserialize(SerDeser.serialize(gen_obj))), [0, 1, 2]
        )
        self.assertEqual(
            list(SerDeserXML.deserialize(SerDeserXML.serialize(gen_obj))), [0, 1, 2]
        )

    def test_iterator(self):
        my_list = [1, 2, 3]
        my_iter = iter(my_list)
        self.assertEqual(
            list(SerDeser.deserialize(SerDeser.serialize(my_iter))), my_list
        )
        self.assertEqual(
            list(SerDeserXML.deserialize(SerDeserXML.serialize(my_iter))), my_list
        )

    def test_recursion(self):
        def factorial(n):
            if n == 0:
                return 1
            else:
                return n * factorial(n - 1)

        self.assertEqual(SerDeser.deserialize(SerDeser.serialize(factorial(5))), 120)
        self.assertEqual(
            SerDeserXML.deserialize(SerDeserXML.serialize(factorial(5))), 120
        )

    def test_decorator(self):
        def my_decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs) * 2

            return wrapper

        @my_decorator
        def my_function(x):
            return x + 1

        self.assertEqual(SerDeser.deserialize(SerDeser.serialize(my_function(3))), 8)
        self.assertEqual(
            SerDeserXML.deserialize(SerDeserXML.serialize(my_function(3))), 8
        )


def main():
    unittest.main()


if __name__ == "__main__":
    main()
