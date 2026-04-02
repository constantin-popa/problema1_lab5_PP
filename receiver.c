#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <string.h>
#include <regex.h>
#include <stdlib.h>


struct mesg_buffer {
    long mesg_type;
    char mesg_text[2048];
} message;

int main(){
    key_t key;
    int msgid;
    regex_t regex;
    int regex_result;
    FILE *fisier;

    key = 123321;
    const char *pattern = "^[[:space:]]*<!DOCTYPE html>[[:space:]]*<head>[[:space:]]*<meta charset=\"UTF-8\">[[:space:]]*<title>[^<]*</title>[[:space:]]*</head>[[:space:]]*<body>[[:space:]]*<h1>[^<]*</h1>([[:space:]]*<p>[^<]*</p>)*[[:space:]]*</body>[[:space:]]*</html>[[:space:]]*$";

   msgid = msgget(key, 0666 | IPC_CREAT);

   msgrcv(msgid, &message, sizeof(message), 1, 0);
   printf("Data Received is : %s \n", message.mesg_text);

   if( regcomp(&regex, pattern, REG_EXTENDED) != 0)
   {
        printf("Eroare la expresia regulata\n");
        exit(1);
   }

   regex_result = regexec(&regex, message.mesg_text, 0, NULL, 0);

   if(regex_result == 0)
   {
        fisier = fopen("mesaj_salvat.html", "w+");
        if(fisier == NULL)
        {
            printf("Nu s a putut deschide fisierul\n");
            exit(1);
        }
        fprintf(fisier, "%s\n", message.mesg_text);
        fclose(fisier);
        printf("Mesajul a fost salvat cu succes\n");
   }
   else if(regex_result == REG_NOMATCH)
   {
        printf("Validare regex esuata\n");
   }

   regfree(&regex);
   msgctl(msgid, IPC_RMID, NULL);
return 0;
}
