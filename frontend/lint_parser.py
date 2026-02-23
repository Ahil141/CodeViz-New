import subprocess
import json
import os

def run_lint():
    try:
        # Run eslint on src directory and output JSON
        result = subprocess.run(
            ['npx', 'eslint', 'src', '--format', 'json'],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if not result.stdout.strip():
            print("No output from eslint.")
            return

        # Parse the JSON output
        try:
            lint_data = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            # If stdout has extra text before JSON, try to find the start
            start = result.stdout.find('[')
            if start != -1:
                lint_data = json.loads(result.stdout[start:])
            else:
                print(f"Failed to parse JSON: {e}")
                print(f"Raw output: {result.stdout[:500]}...")
                return

        with open('lint_summary.txt', 'w') as f:
            for entry in lint_data:
                messages = entry.get('messages', [])
                if not messages:
                    continue
                
                f.write(f"\nFile: {entry['filePath']}\n")
                for msg in messages:
                    severity = "Error" if msg['severity'] == 2 else "Warning"
                    f.write(f"  {severity} ({msg['line']}:{msg['column']}): {msg['message']} [{msg.get('ruleId')}]\n")
        print("Done writing to lint_summary.txt")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_lint()
