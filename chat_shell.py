import os
from core.command_generator import generate_command
from core.command_explainer import explain_command
from core.command_executor import execute_command
from core.output_summarizer import summarize_output
from core.safety_guard import is_command_dangerous, danger_reason
from core.context_manager import ContextManager

def main():
    print("🤖 Welcome to your AI-powered CLI Assistant!")
    print("Type 'exit' to quit.\n")

    context = ContextManager()
    current_dir = os.getcwd()

    while True:
        # 1️⃣ Get user instruction
        instruction = input("🔍 What do you want to do? ")

        if instruction.strip().lower() in ["exit", "quit"]:
            print("👋 Exiting. Have a productive day!")
            break

        # 2️⃣ Generate shell command
        shell_command = generate_command(instruction)
        print(f"\n⚙️ Generated Command: {shell_command}")

        # 3️⃣ Handle `cd` manually to maintain session directory
        if shell_command.strip().lower().startswith("cd "):
            parts = shell_command.strip().split(maxsplit=1)
            if len(parts) == 2:
                new_path = os.path.abspath(os.path.join(current_dir, parts[1]))
                if os.path.isdir(new_path):
                    current_dir = new_path
                    print(f"📂 Changed directory to: {current_dir}")
                else:
                    print(f"⚠️ Directory not found: {new_path}")
            continue

        # 4️⃣ Explain command if user wants
        explain = input("❓ Do you want an explanation? (y/n): ").lower()
        if explain == "y":
            explanation = explain_command(shell_command)
            print(f"\n📘 Explanation:\n{explanation}")

        # 5️⃣ Safety check with override
        is_danger = is_command_dangerous(shell_command)
        if is_danger:
            print(f"\n⚠️ Warning: Dangerous command detected!")
            print(f"{danger_reason(shell_command)}")
            confirm = input("⚠️ Are you sure you want to run it? (y/n): ").lower()
            if confirm != "y":
                print("❌ Skipping dangerous command.\n")
                continue
        else:
            confirm = input("✅ Run this command? (y/n): ").lower()
            if confirm != "y":
                print("❌ Command skipped.\n")
                continue

        # 6️⃣ Execute the command
        result = execute_command(shell_command, cwd=current_dir)
        if result["success"]:
            print(f"\n📤 Output:\n{result['output']}")
        else:
            print(f"\n❌ Error:\n{result['error']}")

        # 7️⃣ Ask to summarize output
        if result["success"] and result["output"]:
            want_summary = input("\n📝 Summarize output? (y/n): ").lower()
            if want_summary == 'y':
                summary = summarize_output(shell_command, result["output"])
                print(f"\n🧠 Summary:\n{summary}")
            else:
                summary = ""
        else:
            summary = ""

        # 8️⃣ Save to context
        context.add(instruction, shell_command, result["output"])

        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    main()
