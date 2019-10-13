#include <cpp_redis/cpp_redis>
#include <tacopie/tacopie>

#include <condition_variable>
#include <iostream>
#include <mutex>
#include <signal.h>

using namespace std;
std::condition_variable should_exit;

void sigint_handler(int) {
  should_exit.notify_all();
}

int main( int argc, char* argv[]) {


  // Enable logging
  cpp_redis::active_logger = std::unique_ptr<cpp_redis::logger>(new cpp_redis::logger);

  cpp_redis::subscriber sub;


  sub.connect("127.0.0.1", 7001 , [](const std::string& host, std::size_t port, cpp_redis::subscriber::connect_state status) {
    if (status == cpp_redis::subscriber::connect_state::dropped) {
      std::cout << "client disconnected from " << host << ":" << port << std::endl;
      should_exit.notify_all();
    }
  });

  string chan("CH1");
  if ( argc > 1 )
  {
    chan = std::string(argv[1]);
    cout<<"INFO: Subscribing to a channel "<<chan<<endl;
  }
  
  sub.subscribe(chan, [](const std::string& chan, const std::string& msg) {
    std::cout << "MESSAGE " << chan << ": " << msg << std::endl;
  });
  sub.psubscribe("*", [](const std::string& chan, const std::string& msg) {
    std::cout << "PMESSAGE " << chan << ": " << msg << std::endl;
  });
  sub.commit();

  signal(SIGINT, &sigint_handler);
  std::mutex mtx;
  std::unique_lock<std::mutex> l(mtx);
  should_exit.wait(l);

  return 0;
}
