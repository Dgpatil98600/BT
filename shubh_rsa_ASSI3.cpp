#include <iostream>
#include <vector>
#include <utility>
#include <cstdlib>
#include <ctime>
#include <fstream>
using namespace std;

string asciiVectorToWord(const vector<int>& asciiValues) {
    string result = "";
    for (int val : asciiValues) {
        result += static_cast<char>(val);
    }
    return result;
}

bool isPrime(int n) {
    if (n <= 1)
        return false;
    if (n <= 3)
        return true;

    if (n % 2 == 0 || n % 3 == 0)
        return false;

    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
    }
    return true;
}


vector<pair<int, int>> getOddPairs(int minProd = 128, int maxProd = 255)
{
    vector<pair<int, int>> pairs;

    for (int i = 3; i < maxProd; i += 2) 
    {
        for (int j = i; j < maxProd; j += 2)
        {
            int product = i * j;

            if (product > minProd && product < maxProd)
            {
                pairs.push_back({i, j});
            }
        }
    }

    return pairs;
}

int find_d(int e, int fi_n)
{
    for (int d = 1; d < fi_n; d++)
    {
        if ((e * d) % fi_n == 1)
        {
            return d;
        }
    }
    return -1;
}

int gcd(int a, int b)
{
    while (b != 0)
    {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

vector<int> find_ascii_value(string message)
{
    vector<int> temp;
    for (char character : message)
    {
        temp.push_back(static_cast<int>(character));
    }
    return temp;
}

int find_e(int p, int q)
{
    int fi_n = (p - 1) * (q - 1);
    int e = 3;

    while (gcd(e, fi_n) != 1)
    {
        e++;
    }
    return e;
}

int find_n(int p, int q)
{
    return p * q;
}

int find_fi_n(int p, int q)
{
    return (p - 1) * (q - 1);
}

int mod_exp(int base, int exp, int mod)
{
    int result = 1;
    for (int i = 0; i < exp; i++)
    {
        result = (result * base) % mod;
    }
    return result;
}


void find_keys(string message)
{
    vector<pair<int, int>> oddPairs = getOddPairs();

    if (oddPairs.empty())
    {
        cout << "No valid odd pairs found!" << endl;
        return;
    }

    cout << "All Possible Odd Pairs (Product between 128 and 255):\n";
    for (auto &pair : oddPairs)
    {
        cout << "(" << pair.first << ", " << pair.second << ") ";
    }
    cout << "\n\n";

    // Random selection
    srand(time(nullptr));
    pair<int, int> selectedPair = oddPairs[rand() % oddPairs.size()];

    int p = selectedPair.first;
    int q = selectedPair.second;

    cout << "Selected Pair: (" << p << ", " << q << ")" << endl;

    int n = find_n(p, q);
    int e = find_e(p, q);
    int d = find_d(e, find_fi_n(p, q));

    cout << "Public Key : (" << e << "," << n << ")" << endl;
    cout << "Private Key : (" << d << "," << n << ")" << endl;
}

void Encrypt_Message(string message)
{
    int public_key_e, public_key_n;

    cout << "Enter Public Key (e,n) : ";
    cin >> public_key_e >> public_key_n;

    vector<int> message_v = find_ascii_value(message);

    cout << "Encrypted Message is : ";
    for (int val : message_v)
    {
        int c = mod_exp(val, public_key_e, public_key_n);
        cout << c << " ";
    }
    cout << endl;
}

void Decrypt_Message(int length)
{
    int d_message;
    int private_key_e, private_key_n;

    cout << "Enter Private Key (e,n) : ";
    cin >> private_key_e >> private_key_n;

    vector<int> dec_message;

    cout << "Enter the Encrypted message : ";
    for (int i = 0; i < length; i++)
    {
        cin >> d_message;
        int c = mod_exp(d_message, private_key_e, private_key_n);
        dec_message.push_back(c);
    }

    cout << "Decrypted Message (ASCII) : ";
    for (int val : dec_message)
    {
        cout << val << " ";
    }
    cout << endl;

    string final_text = asciiVectorToWord(dec_message);
    cout << "The Final Converted Text is : " << final_text << endl;
}

int main()
{
    int choice;
    string message;

    // Open message.txt file
    ifstream file("message.txt");

    // Check if file opened successfully
    if (!file)
    {
        cout << "Error: Unable to open message.txt" << endl;
        return 1;
    }

    // Read message from file
    getline(file, message);

    // Close file
    file.close();

    cout << "Message Read From File: " << message << endl;

    int length = message.length();

    do
    {
        cout << "\nChoose Operation:\n";
        cout << "1. Generate Keys (Using Odd Pairs)\n";
        cout << "2. Encrypt Message\n";
        cout << "3. Decrypt Message\n";
        cout << "4. Exit\n";

        cin >> choice;

        switch (choice)
        {
        case 1:
            find_keys(message);
            break;

        case 2:
            Encrypt_Message(message);
            break;

        case 3:
            Decrypt_Message(length);
            break;

        case 4:
            cout << "Exiting Program\n";
            break;

        default:
            cout << "Invalid choice\n";
        }

    } while (choice != 4);

    return 0;
}