import random


def generateCode(length: int) -> str:
	chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPRQSTUVWXYZ0123456789"
	code = ''.join(random.sample(chars, len(chars)))
	return code[0:length]


if __name__ == '__main__':
	generateCode(10)
