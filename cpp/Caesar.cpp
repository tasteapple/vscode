#include <iostream>


int main()
{
	char a[] = "OAFLWJNSUSLAGF";

	int n = 14;

	for (int key = 0; key < 26; key++) {
		std::cout << "key: " << key << ", ";
		for (int i = 0; i < n; i++) {
			char tmp = 'A' + (a[i] - 'A' - key + 26) % 26;
			std::cout << tmp;
		}
		std::cout << '\n';
	}
}

