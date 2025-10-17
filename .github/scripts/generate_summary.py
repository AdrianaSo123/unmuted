#!/usr/bin/env python3
"""Generate validation summary for GitHub Actions"""

import json
import sys

def main():
    try:
        with open('validation-report.json') as f:
            data = json.load(f)
            summary = data['summary']
        
        print("### Overall Status")
        print(f"- **Tests Run**: {summary['total_tests']}")
        print(f"- **Passed**: ✅ {summary['passed']}")
        
        failed_str = f"❌ {summary['failed']}" if summary['failed'] > 0 else "✅ 0"
        print(f"- **Failed**: {failed_str}")
        
        errors_str = f"🔴 {summary['total_errors']}" if summary['total_errors'] > 0 else "✅ 0"
        print(f"- **Errors**: {errors_str}")
        
        warnings_str = f"⚠️ {summary['total_warnings']}" if summary['total_warnings'] > 0 else "✅ 0"
        print(f"- **Warnings**: {warnings_str}")
        print()
        
        if summary['total_errors'] == 0:
            print("### ✅ All Quality Gates Passed!")
        else:
            print("### ⚠️ Quality Issues Found")
            print()
            print("Check the detailed report artifact for more information.")
            
    except Exception as e:
        print(f"Error generating summary: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
