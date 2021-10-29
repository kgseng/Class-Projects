/* Author: Kenny Seng
*  Date: 11/1/2020
*  Class: CS 344
*  Assignment 3: smallsh Portfolio Assignment
*  Program Description: This program acts as a shell in C, implementing features in well-known shells.
*  The program is capable of providing a prompt for running commands, handling blank lines and comments (lines beginning with '#').
*  Program is also capable of redirecting standard input/output, implementing foreground/background processes, and has three built in commands:
*  cd, exit, and status.
*/

// If you are not compiling with the gcc option --std=gnu99, then
// uncomment the following line or you might get a compiler warning
#define _GNU_SOURCE

#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <signal.h>


// Command line has a maximum length of 2048 characters, 512 arguments
#define CHAR_LIM 2048
#define ARG_LIM 512

// Global foreground flag
int fgFlag = 0;


/* expandVar(char* token, int shellPid):
*  Expands any instance of '%%' in a command into the process ID of smallsh itself.
*/
void expandVar(char* token, int shellPid) {
	char shellStringPid[255];
	char buffer[CHAR_LIM];
	char* temp = token;

	// smallsh process ID -> string
	sprintf(shellStringPid, "%d", shellPid);

	// Copies string up to "$$"
	while ((temp == strstr(temp, "$$"))) {
		strncpy(buffer, temp, temp - token);
		buffer[temp - token] = '\0';
		strcat(buffer, shellStringPid);
		strcat(buffer, temp + strlen("$$"));
		strcpy(token, buffer);
		temp++;
	}
}


/* getStatus(int status):
*  Takes an int and prints the exit status or the terminating signal of the last foreground process ran by the shell.
*  If command is run before any foreground is run, returns exit status 0
*/
void getStatus(int status) {
	// Terminated Normally
	if (WIFEXITED(status)) {
		printf("exit value %d\n", WEXITSTATUS(status));
		fflush(stdout);
	}
	// Terminated via signal
	else {
		printf("terminated by signal %d\n", status);
		fflush(stdout);
	}
}


/* changeDir(char** dirArray):
*  With no arguments, changeDir changes the directory to the specified HOME environment variable
*  If specified, will change the directory to the one specified in dirArray[1]
*/
void changeDir(char** dirArray) {
	// No arguments; change directory to specified HOME environment variable
	if (dirArray[1] == NULL) {
		chdir(getenv("HOME"));
	}
	// Change directory to specified dir
	else {
		chdir(dirArray[1]);
	}
}


/* endBack(pid_t backPid[], int numPid):
*  Ends all background processes via SIGTERM
*/
void endBack(pid_t backPid[], int numPid) {
	int n = 0;
	while (n < numPid) {
		kill(backPid[n], SIGTERM);
		n++;
	}
}


/* handle_SIGTSTP(int signo):
*  Handler for SIGTSTP signals (CTR-Z)
*  If program is in normal mode, SIGTSTP signal switches to foreground-only mode
*  If program is in foreground-only mode, SIGSTP signal switches to normal mode
*/
void handle_SIGTSTP(int signo) {
	// Normal Mode -> Foreground-Only Mode
	// Notifies user that & is ignored in foreground-only mode.
	if (fgFlag == 0) {
		char* message = "Entering foreground-only mode (& is now ignored)\n";
		write(STDOUT_FILENO, message, 50);
		fflush(stdout);
		fgFlag = 1;
	}
	// Foreground-Only Mode -> Normal Mode
	else {
		char* message = "Exiting foreground-only mode\n";
		write(STDOUT_FILENO, message, 30);
		fflush(stdout);
		fgFlag = 0;
	}
}


int main() {
	// User input
	char* cmdLine = malloc(CHAR_LIM);

	// Argument array
	char* argArray[ARG_LIM];

	// To store input file name
	char* inputFile = NULL;
	// To store output file name
	char* outputFile = NULL;

	// Array for background process IDs
	pid_t backPid[512];
	int numPid = 0;
	int status = 0;
	int pid;

	// Background flag
	int bgFlag = 0;
	int numChars;
	// Token for user input
	char* currToken = NULL;
	char expandLine[CHAR_LIM];
	// Input/output flags
	int input = -1;
	int output = -1;

	// Made with and adapted from Exploration: Signal Handling API, replit 5_3
	// Signal Handler to ignore CTR-C
	// Initialize SIGINT_action struct to be empty
	struct sigaction SIGINT_action = { 0 };
	// Register SIG_IGN as the signal handler
	SIGINT_action.sa_handler = SIG_IGN;
	// Install signal handler
	sigaction(SIGINT, &SIGINT_action, NULL);

	// Signal Handler for CTR-Z
	// Initialize SIGTSTP_action struct to be empty
	struct sigaction SIGTSTP_action = { 0 };
	// Register handle_SIGTSTP() as the signal handler
	SIGTSTP_action.sa_handler = &handle_SIGTSTP;
	// Reset signal types 
	sigfillset(&SIGTSTP_action.sa_mask);
	// Automatically restart system call after signal handler is done
	SIGTSTP_action.sa_flags = SA_RESTART;
	// Install signal handler
	sigaction(SIGTSTP, &SIGTSTP_action, NULL);

	// Interpreting command lines from smallsh until exit
	while (1) {
		// Reset background flag
		bgFlag = 0;

		// Shell prompt begins with ':' ; flush out output buffers after print
		printf(": ");
		fflush(stdout);

		// User input
		size_t size = 0;
		numChars = getline(&cmdLine, &size, stdin);

		// getline returns -1 upon failure
		// If there is an error, clear it.
		if (numChars == -1) {
			clearerr(stdin);
		}

		// Parse through user input
		int argsCounter = 0;
		// Counter to keep track of number of args
		currToken = strtok(cmdLine, " \n");

		while (currToken != NULL) {
			// Case 1: Output Redirection via '>'
			if (strcmp(currToken, ">") == 0) {
				// Grab the output file name
				currToken = (strtok(NULL, " \n"));
				outputFile = strdup(currToken);
				// Move null pointer
				currToken = strtok(NULL, " \n");
			}
			// Case 2: Input Redirection via '<'
			else if (strcmp(currToken, "<") == 0) {
				// Grab the input file name
				currToken = (strtok(NULL, " \n"));
				inputFile = strdup(currToken);
				// Move null pointer
				currToken = strtok(NULL, " \n");
			}
			// Case 3: Expand '$$' if necessary, otherwise store the argument in the argArray.
			else {
				// Look for '$$'; strstr returns NULL if there is no overlap.
				// If '$$' is present
				if (strstr(currToken, "$$") != NULL) {
					// Replace '$$' with the shell PID
					int shellPid = getpid();
					strcpy(expandLine, currToken);
					expandVar(expandLine, shellPid);
					currToken = expandLine;
				}
				// Token added to argArray
				argArray[argsCounter] = strdup(currToken);
				currToken = strtok(NULL, " \n");
				argsCounter++;
			}
		}
		// Look at the last argument to determine if it is an '&'
		// If the last argument is an &, it must be executed in the background
		argsCounter--;
		// If the last argument is '&' and the argument is not null
		if (strcmp(argArray[argsCounter], "&") == 0 && argArray[argsCounter] != NULL) {
			// Remove '&' and set bgFlag
			argArray[argsCounter] = '\0';
			// If we are in normal mode, set the flag
			// If we are in foreground only mode, then no background processes can be executed
			if (fgFlag == 0) {
				bgFlag = 1;
			}
		}
		// Undo decrement 
		argsCounter++;
		// End array value with NULL
		argArray[argsCounter] = NULL;

		// Now that we have our command stored, we can compare it to our built-in commands

		fflush(stdout);
		// Case 1: Blank Lines or Comments
		// If the argument is NULL or the argument starts with '#'
		if (argArray[0] == NULL || strncmp(argArray[0], "#", 1)== 0) {
			// Nothing is done
		}

		// Case 2: 'status'
		else if (strcmp(argArray[0], "status") == 0) {
			// Call getStatus() & flush output
			getStatus(status);
			fflush(stdout);
		}

		// Case 3: 'cd'
		else if (strcmp(argArray[0], "cd") == 0) {
			// Call changeDir()
			changeDir(argArray);
		}

		// Case 4: 'exit'
		else if (strcmp(argArray[0], "exit") == 0) {
			// Call endBack()
			endBack(backPid, numPid);
			exit(EXIT_SUCCESS);
		}

		// Otherwise it is not a built-in command; will execute via execvp, and by forking a child process
		else {
			pid = fork();

			// Child Process
			//	Children running in background must ignore SIGINT
			//	Children running in foreground must terminate self while receiving SIGINT
			// Child Processes inherently ignore SIGINT, so the SIGINT handler must be reset to allow for termination.
				if (pid == 0) {
				// Child process is in the foreground
				if (bgFlag == 0) {
					SIGINT_action.sa_handler = SIG_DFL;
					sigaction(SIGINT, &SIGINT_action, NULL);
				}
				// Input redirection specified; open in read-only
				// If it cannot open, print error message, flush, and set exit status to 1
				if (inputFile != NULL) {
					input = open(inputFile, O_RDONLY);
					if (input == -1) {
						fprintf(stderr, "cannot open %s for input\n", inputFile);
						fflush(stdout);
						exit(1);
					}
					// Redirect input
					dup2(input, 0);
					// Close Input File
					close(input);
				}

				// Output redirection specified; open in write-only
				// If it cannot open, print error message, flush, and set exit status to 1
				if (outputFile != NULL) {
					output = open(outputFile, O_WRONLY | O_CREAT | O_TRUNC, 0666);
					if (output == -1) {
						fprintf(stderr, "cannot open %s for output\n", outputFile);
						fflush(stdout);
						exit(1);
					}
					// Redirect input
					dup2(output, 1);
					// Close Output File
					close(output);
				}
				// Child Process is in the background
				// If user does not redirect standard input for a background command, redirect to /dev/null
				if (bgFlag == 1) {
					if (inputFile == NULL) {
						input = open("/dev/null", O_RDONLY);
						if (input == -1) {
							fprintf(stderr, "cannot open /dev/null/ for input \n");
							fflush(stdout);
							exit(1);
						}
						// Redirect input
						dup2(input, 0);
						// Close Input File
						close(input);
					}
					// If user does not redirect standard output for a background command, redirect to /dev/null
					if (outputFile == NULL) {
						output = open("/dev/null", O_WRONLY);
						if (output == -1) {
							fprintf(stderr, "cannot open /dev/null for output \n");
							fflush(stdout);
							exit(1);
						}
						// Redirect Output File
						dup2(output, 1);
						// Close Output File
						close(output);
					}
				}
				//Execute command; print an error message if command is not found
				if (execvp(argArray[0], argArray)) {
					fprintf(stderr, "%s: no such file or directory\n", argArray[0]);
					fflush(stdout);
					exit(1);
				}

			}
			// Parent Process
			else {
				// Process is in the foreground
				if (bgFlag == 0) {
					// Wait for process to finish
					pid = waitpid(pid, &status, 0);

					// If process is terminated, print error message and terminating signal
					if (WIFSIGNALED(status)) {
						printf("terminated by signal %d\n", status);
						fflush(stdout);
					}
				}
				// Process is in the background
				if (bgFlag == 1) {
					// Do not wait for process to finish
					waitpid(pid, &status, WNOHANG);

					// Add process id to background PID array
					backPid[numPid] = pid;
					numPid++;
					// Print message with added background process ID
					printf("background pid is %d\n", pid);
					fflush(stdout);
				}
			}
		}

		// Command has been executed; must reset for the next command
		// Clear out the Argument Array
		int j = 0;
		while (j < argsCounter) {
			argArray[j] = NULL;
			j++;
		}

		// Clear out input/output files
		inputFile = NULL;
		outputFile = NULL;

		// Clear out user input
		cmdLine = NULL;
		free(cmdLine);

		// Check background processes that have completed and that have been terminated
		pid = waitpid(-1, &status, WNOHANG);
		while (pid > 0) {
			// Print process ID and exit value upon ending normally
			if (WIFEXITED(status)) {
				printf("background pid %d is done: exit value %d\n", pid, status);
				fflush(stdout);
			}
			// Print process ID and signal upon being terminated
			else {
				printf("background pid %d is done: terminated by signal %d\n", pid, status);
				fflush(stdout);
			}
			// Keep checking
			pid = waitpid(-1, &status, WNOHANG);
		}
	}
	return 0;
}
