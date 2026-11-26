#include <array>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct Student {
    std::string id;
    std::string name;
    int grade;
};

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::vector<Student> students;
    std::map<std::string, std::size_t> by_id;
    std::map<std::string, std::size_t> by_name;
    std::array<std::vector<std::size_t>, 101> by_grade;

    const auto print = [&](std::size_t index) {
        const auto& student = students[index];
        std::cout << student.id << ' ' << student.name << ' '
                  << student.grade << '\n';
    };

    int command;
    while (std::cin >> command) {
        switch (command) {
        case 1: {
            Student student;
            std::cin >> student.id >> student.name >> student.grade;
            const std::size_t index = students.size();
            if (!by_id.emplace(student.id, index).second) {
                std::cout << "FAILED\n";
                break;
            }
            by_name.emplace(student.name, index);
            by_grade[student.grade].push_back(index);
            students.push_back(student);
            std::cout << "SUCCESS\n";
            break;
        }
        case 2:
            for (std::size_t i = 0; i < students.size(); ++i) {
                print(i);
            }
            break;
        case 3: {
            std::string id;
            std::cin >> id;
            print(by_id.at(id));
            break;
        }
        case 4: {
            std::string name;
            std::cin >> name;
            print(by_name.at(name));
            break;
        }
        case 5:
            // All IDs have nine digits, so string order is numeric order.
            for (const auto& entry : by_id) {
                print(entry.second);
            }
            break;
        case 6:
            for (int grade = 100; grade >= 0; --grade) {
                for (std::size_t index : by_grade[grade]) {
                    print(index);
                }
            }
            break;
        case 7:
            std::cout << "END\n";
            return 0;
        }
    }
}
