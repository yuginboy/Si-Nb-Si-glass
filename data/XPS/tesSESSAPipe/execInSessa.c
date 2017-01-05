//SESSA_WINDOWS.c /Calling SESSA on the Windows operating system
//1.) Variable Declarations
#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define BUFSIZE 1024
HANDLE hFile;
char buffer[BUFSIZE];

//F1.) Function to actually relay a command toSESSA

void WriteToPipe(char* message)
{
  DWORD dwWrite;
  BOOL success;

  printf("Sending message %s to pipe\n", message);
  strcpy(buffer, message);
  strcat(buffer, "\n");
  success = WriteFile(hFile, buffer, strlen(buffer), &dwWrite, NULL);
  if(!success) {
      printf("WriteFile to pipe failed (%s, GLE=%d)\n", message, GetLastError() );
      exit(-1);
  }
}
//F2.) Clear Buffer and wait
void WaitForCommand()
{
  BOOL success, finished;
  DWORD cbRead;
  do {
      success = ReadFile(hFile,		// pipe handle
			  buffer, 	// buffer to receive reply
			  BUFSIZE, 	// size of buffer
			  &cbRead, 	// number of bytes read
			  NULL);	// not overlapped
      if(!success && GetLastError()!=ERROR_MORE_DATA)
	    break;
      buffer[cbRead] = '\0';
      printf("Sessa: %s", buffer);
      finished = strstr(buffer, "Done")!=NULL;
  } while(!success || !finished);// repeat loop if ERROR_MORE_DATA
}

char* concat(const char* str1, const char* str2)
{
    char* result;
    asprintf(&result, "%s%s", str1, str2);
    return result;
}

int main(int argc, char **argv)
{ 
//   const char *const startCommand = "PROJECT LOAD SESSION = \"";
  const char *const startCommand = " ";
  const char *const endCommand = " ";
//   printf("%s%s%s\n",startCommand, argv[1], endCommand);
  char* resCmd = concat(concat(startCommand,argv[1]), endCommand);
//   printf("-> %s\n", resCmd);
  FILE* fp;

//2.) Open the pipe to SESSA
  hFile =CreateFile("\\\\.\\pipe\\SessaPipe",
			 GENERIC_WRITE | GENERIC_READ,
			  0,
			  NULL,
			  OPEN_EXISTING,
			  0,
			  NULL);
  if(hFile == INVALID_HANDLE_VALUE) {
      printf("CreateFile failed for Named Pipe client\n" );
      exit(-1);
    
  }
      
//3.) Pass CLI commands to SESSA
  WriteToPipe(resCmd);
  WaitForCommand();
//   WriteToPipe("PROJECT RESET");
//   WaitForCommand();
// WriteToPipe("PROJECT RESET");
// WaitForCommand();
// WriteToPipe("SAMPLE SET MATERIAL /Si/O2/ LAYER 1"); WaitForCommand();
// WriteToPipe("MODEL SIMULATE");
// WaitForCommand();
// WriteToPipe("SAMPLE PEAK PLOT PART_INT PEAK 1"); WaitForCommand();
// WriteToPipe("PLOT SAVE DATA \"C:\\Temp\\Si2s.txt\""); WaitForCommand();
  WriteToPipe("QUIT");
  WaitForCommand();
  CloseHandle(hFile);

//4.) Open the SESSA output for further analysis
//   fp = fopen("C:\\Temp\\Si2s.txt", "r");
//   if(fp==NULL) {
//       puts("Error: cannot open data file.");
//       exit(-1);
//   } else {
//       puts("Showing partial intensities for the Si2s peak");
//       puts("n\t\tC_n");
//       while(fgets(buffer, BUFSIZE, fp)!=NULL) {
// 	      double x, y;
// 	      if(buffer[0]=='#')
// 		  continue;
// 	      fscanf(fp, "%le %le", &x, &y );
// 	      printf("%le\t%le\n", x, y);
//   }
//   fclose(fp);
// }
}