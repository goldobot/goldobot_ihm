#include <stdio.h>
#include <errno.h>
#include <fcntl.h> 
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include <zmq.h>
#include <math.h>

unsigned char buff[0x100000];

char fname[256];

char zmq_addr_buff[64];

int port_nb = 3101;

int main(int argc, const char * argv[])
{
  int rc;

  if (argc!=2) {
    printf (" %s <fname>\n", argv[0]);
    return -1;
  }

  memset(buff, 0, sizeof(buff));

  strncpy(fname, argv[1], sizeof(fname));

  FILE *fp = fopen(fname, "rb");
  if (fp==NULL) {
    printf (" cannot open %s\n", fname);
    return -1;
  }

  int nread = fread(buff, 1, sizeof(buff), fp);
  if (nread==0) {
    printf (" cannot read %s\n", fname);
    printf (" ferror()=%d\n", ferror(fp));
    //return -1;
  } else {
    printf (" read %d bytes\n", nread);
  }

  for (int i=0; i<4; i++) {
    for (int j=0; j<16; j++) {
      printf (" %.2x", buff[j+16*i]);
    }
    printf ("\n");
  }

  void* m_zmq_context;
  void* m_pub_socket;

  m_zmq_context = zmq_init(1);
  printf (" created ZMQ context\n");

  m_pub_socket = zmq_socket(m_zmq_context, ZMQ_PUB);
  if (m_pub_socket<0) {
    printf (" cannot create ZMQ_PUB socket\n");
    return -1;
  }
  printf (" created ZMQ socket\n");

  sprintf(zmq_addr_buff, "tcp://127.0.0.1:%d", port_nb);
  //printf("  ZMQ DEBUG: zmq_addr_buff = %s\n", zmq_addr_buff);
  rc = zmq_bind(m_pub_socket, zmq_addr_buff);
  if (rc<0) {
    printf (" cannot bind ZMQ_PUB socket\n");
    return -1;
  }
  printf (" bind ZMQ socket\n");

  unsigned short my_message_type = 2051;
  unsigned char compress_flag = 0;

  fgetc(stdin);

  printf (" sending data..\n");

  zmq_send (m_pub_socket, (const char*)(&my_message_type), 2, ZMQ_SNDMORE);
  zmq_send (m_pub_socket, (const char*)(&compress_flag), 1, ZMQ_SNDMORE);
  zmq_send (m_pub_socket, buff, nread, 0);


  sleep(1);


  //zmq_term(m_zmq_context);

  zmq_close(m_pub_socket);

  fclose(fp);

  return 0;
}


