#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

int tcp_socket() {
    return socket(AF_INET, SOCK_STREAM, 0);
}

int tcp_connect(int sockfd, const char* host, int port) {
    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port);

    if (inet_pton(AF_INET, host, &serv_addr.sin_addr) <= 0) {
        return -1; // Invalid address
    }

    return connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
}

int tcp_send(int sockfd, const char* data) {
    return send(sockfd, data, strlen(data), 0);
}

int tcp_recv(int sockfd, char* buffer, int size) {
    return recv(sockfd, buffer, size - 1, 0);
}

void tcp_close(int sockfd) {
    close(sockfd);
}
