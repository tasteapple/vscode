#include <iostream>
#include <fstream>
using namespace std;

int main() {
	ifstream fin; fin.open("input.txt");
	char a[2076];
	int cnt[26][26][26] = { 0, };
	int l = 0;
	for (int i = 0; i < 2076; i++) {
		char x; fin.get(x);
		if ('a' <= x && x <= 'z') {
			a[l] = x;
			l++;
		}
	}
	for (int i = 0; i < l - 3; i++) cnt[a[i] - 'a'][a[i + 1] - 'a'][a[i + 2] - 'a']++;

	for (int i = 0; i < 26; i++) {
		for (int j = 0; j < 26; j++) {
			for (int k = 0; k < 26; k++) {
				if (cnt[i][j][k] > 5) cout << (char)('a' + i) << ' ' << (char)('a' + j) << ' ' << (char)('a' + k) << ": " << cnt[i][j][k] << '\n';
			}
		}
	}
	cout << '\n';

	int idx[14];
	cout << "indices of gjs: ";
	int cnt2 = 0;
	for (int i = 0; i < l - 3; i++) {
		if (a[i] == 'g' && a[i + 1] == 'j' && a[i + 2] == 's') {
			idx[cnt2] = i;
			cnt2++;
			cout << i << ' ';
		}
	}
	cout << '\n' << '\n';

	cout << "distances between indices of gjs: ";
	for (int i = 0; i < 13; i++) {
		cout << idx[i + 1] - idx[i] << ' ';
	}
	cout << '\n' << '\n';

	int cnt3[4][26] = { 0, };
	for (int i = 0; i < l; i++) {
		cnt3[i % 4][a[i] - 'a']++;
	}

	for (int i = 0; i < 4; i++) {
		cout << i << "-th group alphabet count:\n";
		for (int j = 0; j < 26; j++) {
			cout << (char)('a' + j) << ": " << cnt3[i][j] << (j == 25 ? ' ':',') << ' ';
		}
		cout << '\n';
	}
	cout << '\n';


	for (int i = 0; i < l; i++) {
		if (i % 4 == 0) cout << (char)('a' + ((a[i] - 'a') + ('e' - 'g') + 26) % 26);
		if (i % 4 == 1) cout << (char)('a' + ((a[i] - 'a') + ('e' - 's') + 26) % 26);
		if (i % 4 == 2) cout << (char)('a' + ((a[i] - 'a') + ('e' - 'k') + 26) % 26);
		if (i % 4 == 3) cout << (char)('a' + ((a[i] - 'a') + ('e' - 'r') + 26) % 26);
	}
	cout << '\n' << '\n';

	for (int i = 0; i < l; i++) {
		if (i % 4 == 0) cout << (char)('a' + ((a[i] - 'a') + ('e' - 'g') + 26) % 26);
		if (i % 4 == 1) cout << (char)('a' + ((a[i] - 'a') + ('e' - 's') + 26) % 26);
		if (i % 4 == 2) cout << (char)('a' + ((a[i] - 'a') + ('e' - 'v') + 26) % 26);
		if (i % 4 == 3) cout << (char)('a' + ((a[i] - 'a') + ('e' - 'r') + 26) % 26);
	}
	cout << '\n' << '\n';

	cout << "key: "
		<< (char)('a' + ('g' - 'e' + 26) % 26)
		<< (char)('a' + ('s' - 'e' + 26) % 26)
		<< (char)('a' + ('v' - 'e' + 26) % 26)
		<< (char)('a' + ('r' - 'e' + 26) % 26)
		<< '\n';
}

