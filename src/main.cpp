#include <iostream>
#include <vector>
#include <string>

// Placeholder for interpreter loop
void run_repl() {
    std::string input;
    std::cout << "AI-APL Interpreter (v0.1.0)" << std::endl;
    std::cout << "Type 'exit' to quit." << std::endl;

    while (true) {
        std::cout << "      "; // APL standard prompt indentation
        std::getline(std::cin, input);

        if (input == "exit") {
            break;
        }

        // TODO: Parse and evaluate APL expression
        std::cout << "Echo: " << input << std::endl;
    }
}

int main(int argc, char* argv[]) {
    // TODO: Handle command line arguments (e.g., load file)
    
    run_repl();

    return 0;
}
