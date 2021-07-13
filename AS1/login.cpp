#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <stdint.h>
#include <unistd.h>
#include <time.h>
using namespace std;

void login1(char *input1, char *input2)
{
	struct
	{
		char username[25];
		char password[25];
		int canary;
		char good_username[25];
		char good_password[25];
		int goodcanary;
	} v;
	v.canary = rand() % 128 + 1;
	v.goodcanary = v.canary;

	//read correct username and password
	FILE *fp = fopen("password.txt", "r");
	fgets(v.good_username, 25, fp);
	fgets(v.good_password, 25, fp);
	fclose(fp);
	v.good_username[strlen(v.good_username) - 1] = '\0';
	v.good_password[strlen(v.good_password) - 1] = '\0';
	strcpy(v.username, input1);
	strcpy(v.password, input2);

	//terminate strings properly for strcmp
	v.username[24] = '\0';
	v.password[24] = '\0';
	v.good_username[24] = '\0';
	v.good_password[24] = '\0';

	//check canary and login success
	if (v.canary != v.goodcanary)
	{
		printf("Stack overflow detected, exiting.\n");
		exit(-1);
	}
	if (strcmp(v.username, v.good_username) == 0 && strcmp(v.password, v.good_password) == 0)
		printf("Login successful!\n");
	else
		printf("Login denied.\n");
}

void login2(char *input1, char *input2)
{
	struct
	{
		int32_t goodcanary; //these are integers now instead of characters
		char password[25];
		int32_t canary;
		char good_username[25];
		char good_password[25];
		char username[25];
	} v;
	v.canary = 'b';
	v.goodcanary = 'b';

	//read correct username and password
	FILE *fp = fopen("password.txt", "r");
	fgets(v.good_username, 25, fp);
	fgets(v.good_password, 25, fp);
	fclose(fp);
	v.good_username[strlen(v.good_username) - 1] = '\0';
	v.good_password[strlen(v.good_password) - 1] = '\0';

	//load username
	strcpy(v.username, input1);

	//set up "random" canary
	//for real code, a buffer overread can allow you to read the true value of canaries
	//canary randomisastion may also be predictable
	//this example demonstrates that
	v.goodcanary = v.username[2] * 256 * 256 * 257 + (v.username[0] - 39) * 256 + 72;
	v.canary = v.goodcanary;

	//load password
	strcpy(v.password, input2);

	//terminate strings properly for strcmp
	v.username[24] = '\0';
	v.password[24] = '\0';
	v.good_username[24] = '\0';
	v.good_password[24] = '\0';

	//check canary and login success
	if (v.canary != v.goodcanary)
	{
		printf("Stack overflow detected, exiting.\n");
		exit(-1);
	}
	if (strcmp(v.username, v.good_username) == 0 && strcmp(v.password, v.good_password) == 0)
		printf("Login successful!\n");
	else
		printf("Login denied.\n");
}

void login3(char *input1, char *input2)
{
	struct
	{
		int32_t goodcanary;
		char username[25];
		char password[25];
		int32_t canary;
		char good_username[25];
		char good_password[25];
	} v;
	v.goodcanary = rand();
	v.canary = v.goodcanary;

	strcpy(v.password, "abcdefghijklmnopqrstuvwx");

	//read correct username and password
	FILE *fp = fopen("password.txt", "r");
	fgets(v.good_username, 25, fp);
	fgets(v.good_password, 25, fp);
	fclose(fp);
	v.good_username[strlen(v.good_username) - 1] = '\0';
	v.good_password[strlen(v.good_password) - 1] = '\0';
	strcpy(v.username, input1);
	//let's load v.password carefully. we only want valid characters.
	int written_char = 0;
	int warn_user = 0;
	int ind = 0;

	while (written_char < 25)
	{ //don't write too much
		int c = (int)input2[ind];
		if (c == 0 || (c >= 48 && c <= 57) || (c >= 65 && c <= 90) || (c >= 97 && c <= 122))
		{
			//this is an okay character. load it
			v.password[ind] = (char)c;
			written_char += 1;
		}
		else if (c == 58 || c == 59)
		{ //sometimes user types some characters by accident. let's remove them.
			v.password[ind] = 0;
			written_char += 1;
		}
		else
		{ //a strange character! let's warn the user, but don't load it
			warn_user = 1;
		}
		if (c == 0)
		{ //reached end of string, terminate
			printf("HELLO MAN INSIDE NULL\n");
			break;
		}
		ind += 1;
	}
	if (warn_user == 1)
	{
		printf("Invalid characters found and skipped. Did you type your password correctly?\n");
	}

	//terminate strings properly
	v.username[24] = '\0';
	v.password[24] = '\0';
	v.good_username[24] = '\0';
	v.good_password[24] = '\0';

	//check canary and login success
	if (v.canary != v.goodcanary)
	{
		printf("Stack overflow detected, exiting.\n");
		exit(-1);
	}
	if (strcmp(v.username, v.good_username) == 0 && strcmp(v.password, v.good_password) == 0)
		printf("Login successful!\n");
	else
		printf("Login denied.\n");
}

int main(int argc, char *argv[])
{
	srand(time(NULL));
	char helpstr[] = "Use: login -? <username> <password> or Use: login -l <filename>\nOptions are: -i, -j, -k, -l (see assignment)\n";
	if (argc < 3)
	{
		printf("%s\n", helpstr);
		return -1;
	}

	if (access("password.txt", F_OK) == -1)
	{
		printf("password.txt not found; please download it and put it in this directory.\n");
		return -1;
	}

	if (strlen(argv[1]) < 2)
	{
		printf("%s\n", helpstr);
		return -1;
	}

	switch (argv[1][1])
	{
	case 'i':
		if (argc < 4)
		{
			printf("%s\n", helpstr);
			break;
		}
		login1(argv[2], argv[3]);
		break;
	case 'j':
		if (argc < 4)
		{
			printf("%s\n", helpstr);
			break;
		}
		login2(argv[2], argv[3]);
		break;
	case 'k':
		if (argc < 4)
		{
			printf("%s\n", helpstr);
			break;
		}
		login3(argv[2], argv[3]);
		break;
	default:
		printf("%s\n", helpstr);
		return -1;
	}
	return 0;
}
