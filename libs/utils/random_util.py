import random


class RandomUtil(object):

    Letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    Numbers = list("0123456789")
    Special_chars = list("~`!@#$%^&* ()_-+=|\\{}[]:;\"',./")

    @classmethod
    def generate_string(cls, length, is_range=False, contain_numbers=False, contain_special_chars=False):
        """
        It is a class method, used to generate a random string, which could include letters(upper and lower),
        numbers, and special chars(accepted by HP bridge backend)
        :param length: the length of the random string which will be generated
        :param is_range: Default is False. if true, the length of the generated random string
                will be 1 to length(first parameter)
        :param contain_numbers: if true, the generated string will contains the numbers
        :param contain_special_chars: if true, the generated string will contains the special chars
        :return:
        """
        source_chars = []
        source_chars.extend(RandomUtil.Letters)
        if contain_numbers:
            source_chars.extend(RandomUtil.Numbers)
        if contain_special_chars:
            source_chars.extend(RandomUtil.Special_chars)
        if is_range:
            length = random.randint(1, length)

        return "".join(random.choices(source_chars, k=length))

    @classmethod
    def generate_numbers(cls, length, is_range=False, start_with_0=False):
        """
        It is a class method, used to generate a random string, which only include numbers
        :param length: the length of the random string which will be generated
        :param is_range: Default is False. if true, the length of the generated random string
                will be 1 to length(first parameter)
        :param start_with_0: Default False. if True, it allows the generated random numbers to start with 0
        :return:
        """
        if is_range:
            length = random.randint(1, length)

        target_strings = "".join(random.choices(RandomUtil.Numbers, k=length))
        if not start_with_0:
            if target_strings.startswith("0"):
                target_strings = random.choice("123456789") + target_strings[1:]

        return target_strings

    @classmethod
    def generate_special_chars(cls, length, is_range=False):
        """
        It is a class method, used to generate a random string, which only include special chars
        :param length: the length of the random string which will be generated
        :param is_range: Default is False. if true, the length of the generated random string
                will be 1 to length(first parameter)
        :return:
        """
        if is_range:
            length = random.randint(1, length)
        return "".join(random.choices(RandomUtil.Special_chars, k=length))

    @classmethod
    def generate_chinese_chars(cls, length, is_range=False, coding="unicode"):
        """
        It is a class method, used to generate a random string, which only include Chinese chars
        :param length: the length of the random string which will be generated
        :param is_range: Default is False. if true, the length of the generated random string
                will be 1 to length(first parameter)
        :param coding: Value of ["unicode", "gb2312"], default is "gb2312", means choosing from 6,000 common Chinese chars.
                if set to "unicode", it means choosing from 20,000 Chinese chars, including the rarely used word.
        :return:
        """
        if is_range:
            length = random.randint(1, length)

        target_string = ""

        if coding.lower() == "gb2312" or coding.lower() == "gbk":
            for _ in range(length):
                head = random.randint(0xb0, 0xf7)
                body = random.randint(0xa1, 0xfe)
                val = f'{head:x}{body:x}'
                target_string += bytes.fromhex(val).decode('gb2312')
        elif coding.lower() == "unicode" or coding.lower() == "utf-8":
            for _ in range(length):
                target_string += chr(random.randint(0x4e00, 0x9fbf))
        else:
            raise KeyError("invalid coding format for " + coding)
        return target_string

    @classmethod
    def generate_string_from(cls, strs, length, is_range=False):
        """
        It is a class method, used to generate a random string, which could include letters(upper and lower),
        numbers, and special chars(accepted by HP bridge backend)
        :param strs: the source chars
        :param length: the length of the random string which will be generated
        :param is_range: Default is False. if true, the length of the generated random string
                will be 1 to length(first parameter)
        :return:
        """
        source_chars = []
        source_chars.extend(strs)
        if is_range:
            length = random.randint(0, length)

        return "".join(random.choices(source_chars, k=length))

    @classmethod
    def generate_boolean(cls):
        """
        generate a boolean value
        :return:
        """
        return random.choice([True, False])

    @classmethod
    def generate_emoji(cls):
        """
        generate a boolean value
        :return:
        """
        return "☺"

