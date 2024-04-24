import pandas as pd


class TrieNode:
	def __init__(self):
		self.children = {}
		self.fail = None
		self.output = []


class AhoCorasick:
	def __init__(self):
		self.root = TrieNode()

	def add_pattern(self, pattern):
		node = self.root
		for char in pattern:
			if char not in node.children:
				node.children[char] = TrieNode()
			node = node.children[char]
		node.output.append(pattern)

	def create_fail_links(self):
		queue = []
		for child in self.root.children.values():
			queue.append(child)
			child.fail = self.root

		while queue:
			node = queue.pop(0)
			for char, child in node.children.items():
				queue.append(child)
				fail_node = node.fail
				while fail_node is not None and char not in fail_node.children:
					fail_node = fail_node.fail
				child.fail = fail_node.children[char] if fail_node else self.root
				child.output += child.fail.output

	def match_count(self, text):
		count = 0
		node = self.root
		for char in text:
			while node is not None and char not in node.children:
				node = node.fail
			if node is None:
				node = self.root
				continue
			node = node.children[char]
			count += len(node.output)
		return count
	
	def match_words(self, text):
		words = []
		node = self.root
		for char in text:
			while node is not None and char not in node.children:
				node = node.fail
			if node is None:
				node = self.root
				continue
			node = node.children[char]

			for i in node.output:
				if not i in words:
					words.append(i)
		return words
