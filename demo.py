"""
Law Changes Demo
Demonstrates processing a single PDF to extract law changes and store in database
"""
from datetime import datetime
import os
import sys

# Add the current directory and subdirectories to sys.path to access modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'services'))
sys.path.insert(0, os.path.join(current_dir, 'utils'))

from services.law_changes_api import LawChangesAPI
from services.database_service import DatabaseService
from utils.pdf_manager import PDFManager


def get_user_input():
    """
    Get PDF file path and associated URL from user input
    """
    print("\n" + "="*60)
    print("LAW CHANGES PROCESSING CONFIGURATION")
    print("="*60)
    
    # Get PDF file path
    print("\nEnter the PDF file to process:")
    print("You can provide either:")
    print("1. Full path to PDF file")
    print("2. Just filename if it's in the pdfs/ directory")
    
    pdf_manager = PDFManager()
    
    while True:
        pdf_input = input("PDF file: ").strip()
        if not pdf_input:
            print("Please enter a PDF file path or filename.")
            continue
        
        # Check if it's a full path
        if os.path.exists(pdf_input):
            pdf_path = pdf_input
            break
        
        # Check if it's a filename in the pdfs directory
        pdf_in_dir = os.path.join(pdf_manager.pdfs_dir, pdf_input)
        if os.path.exists(pdf_in_dir):
            pdf_path = pdf_in_dir
            break
        
        # Check if it's a filename without extension
        if not pdf_input.endswith('.pdf'):
            pdf_with_ext = pdf_input + '.pdf'
            pdf_in_dir_with_ext = os.path.join(pdf_manager.pdfs_dir, pdf_with_ext)
            if os.path.exists(pdf_in_dir_with_ext):
                pdf_path = pdf_in_dir_with_ext
                break
        
        print(f"PDF file not found: {pdf_input}")
        print(f"Checked locations:")
        print(f"  - {pdf_input}")
        print(f"  - {pdf_in_dir}")
        if not pdf_input.endswith('.pdf'):
            print(f"  - {pdf_in_dir_with_ext}")
        print("Please try again.")
    
    # Get associated URL
    print(f"\nPDF found: {pdf_path}")
    print("\nEnter the associated URL for this law document:")
    print("Example: https://legislature.state.gov/bill-2024-123")
    
    while True:
        url = input("URL: ").strip()
        if not url:
            print("Please enter a URL.")
            continue
        
        # Basic URL validation
        if not (url.startswith('http://') or url.startswith('https://')):
            print("URL should start with http:// or https://")
            continue
        
        break
    
    return {
        'pdf_path': pdf_path,
        'url': url
    }


def main():
    """
    Demo of processing a single PDF to extract and store law changes
    """
    print("="*80)
    print("LAW CHANGES EXTRACTION AND STORAGE DEMO")
    print("="*80)
    
    # Initialize PDF manager to show available PDFs
    pdf_manager = PDFManager()
    pdf_paths = pdf_manager.get_pdf_paths()
    
    if pdf_paths:
        print(f"\nAvailable PDFs in directory ({len(pdf_paths)} files):")
        for i, path in enumerate(pdf_paths[:10], 1):  # Show first 10
            print(f"  {i}. {os.path.basename(path)}")
        if len(pdf_paths) > 10:
            print(f"  ... and {len(pdf_paths) - 10} more files")
    else:
        print("\nNo PDF files found in the pdfs directory.")
        print("You can still specify a full path to a PDF file.")
    
    # Get user input for PDF and URL
    config = get_user_input()
    
    print(f"\n" + "="*60)
    print("PROCESSING CONFIGURATION")
    print("="*60)
    print(f"PDF file: {config['pdf_path']}")
    print(f"Associated URL: {config['url']}")
    print(f"PDF filename: {os.path.basename(config['pdf_path'])}")
    
    # Get user confirmation
    input(f"\nPress Enter to start processing...")
    
    # Initialize API service
    print("\nInitializing Law Changes API...")
    try:
        api = LawChangesAPI()
        print("✓ API service initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing API service: {e}")
        return
    
    # Process PDF and store law changes
    print(f"\nProcessing PDF to extract law changes...")
    print("This may take several minutes depending on document size...")
    
    try:
        result = api.process_pdf_and_store(config['pdf_path'], config['url'])
        
        if result['status'] == 'success':
            print("✓ PDF processed successfully!")
            print(f"\n" + "="*60)
            print("PROCESSING RESULTS")
            print("="*60)
            print(f"📄 PDF processed: {result['pdf_filename']}")
            print(f"🔗 Associated URL: {result['url']}")
            print(f"� Law changes stored: {result['records_stored']}")
            
            if result['law_changes']:
                print(f"\n📋 STORED LAW CHANGES:")
                print("-" * 50)
                for i, change in enumerate(result['law_changes'], 1):
                    print(f"{i}. Date: {change['date']}")
                    print(f"   State: {change['state']}")
                    print(f"   Summary: {change['summary']}")
                    print(f"   Database ID: {change['id']}")
                    print()
        
        elif result['status'] == 'warning':
            print(f"⚠️  {result['message']}")
            
        else:
            print(f"✗ Processing failed: {result['message']}")
            return
        
    except Exception as e:
        print(f"✗ Error during processing: {e}")
        return
    
    # Show database statistics
    print(f"\n� DATABASE STATISTICS:")
    print("-" * 50)
    
    try:
        stats = api.get_statistics()
        if stats['status'] == 'success':
            statistics = stats['statistics']
            print(f"Total law changes in database: {statistics['total_law_changes']}")
            print(f"States with changes: {statistics['states_with_changes']}")
            
            if statistics['changes_by_state']:
                print(f"\nChanges by state:")
                for state, count in sorted(statistics['changes_by_state'].items(), 
                                         key=lambda x: x[1], reverse=True):
                    print(f"  • {state}: {count} changes")
        else:
            print(f"Error retrieving statistics: {stats['message']}")
            
    except Exception as e:
        print(f"Error getting database statistics: {e}")
    
    # Show recent law changes
    print(f"\n📚 RECENT LAW CHANGES IN DATABASE:")
    print("-" * 50)
    
    try:
        recent_changes = api.get_law_changes(limit=5)
        if recent_changes['status'] == 'success' and recent_changes['law_changes']:
            for change in recent_changes['law_changes']:
                print(f"Date: {change['date_changed']} | State: {change['state']}")
                summary = change['summary']
                if len(summary) > 80:
                    summary = summary[:77] + "..."
                print(f"Summary: {summary}")
                print(f"URL: {change['url']}")
                print(f"PDF: {change['pdf_filename'] or 'N/A'}")
                print("-" * 30)
        else:
            print("No law changes found in database")
            
    except Exception as e:
        print(f"Error retrieving recent changes: {e}")
    
    # Next steps
    print(f"\n🎯 NEXT STEPS:")
    print("-" * 40)
    print("1. Review the stored law changes in the database")
    print("2. Use the API to query law changes by state or date range")
    print("3. Process additional PDF files to build a comprehensive database")
    print("4. Share findings with legal and compliance teams")
    print("5. Set up automated monitoring for new law changes")
    
    print(f"\n" + "="*80)
    print("LAW CHANGES PROCESSING COMPLETE")
    print("="*80)
    
    # Show database location
    db_path = api.db_service.db_path
    print(f"\n💾 Database location: {db_path}")
    print(f"📈 You can query the database using SQL tools or the API methods")


def quick_demo():
    """
    Quick demo with a predefined PDF from the pdfs directory
    """
    print("="*80)
    print("QUICK DEMO - LAW CHANGES PROCESSING")
    print("="*80)
    
    # Initialize PDF manager and find any available PDF
    pdf_manager = PDFManager()
    pdf_paths = pdf_manager.get_pdf_paths()
    
    if not pdf_paths:
        print("Error: No PDF files found in the pdfs directory.")
        print("\nTo add PDFs:")
        print("1. Copy PDF files directly to the pdfs/ directory")
        print("2. Or run the main demo to specify a full path")
        return
    
    # Use the first available PDF
    pdf_path = pdf_paths[0]
    
    # Sample configuration for quick demo
    sample_url = "https://example.com/sample-law-document"
    
    print(f"Using sample PDF: {os.path.basename(pdf_path)}")
    print(f"Sample URL: {sample_url}")
    
    input("\nPress Enter to start quick processing...")
    
    try:
        # Initialize API and process
        api = LawChangesAPI()
        result = api.process_pdf_and_store(pdf_path, sample_url)
        
        if result['status'] == 'success':
            print("\n✓ Quick processing completed!")
            print(f"Law changes stored: {result['records_stored']}")
            
            # Show some results
            if result['law_changes']:
                print(f"\nSample law changes found:")
                for change in result['law_changes'][:3]:  # Show first 3
                    print(f"• {change['state']} - {change['date']}")
                    print(f"  {change['summary'][:100]}...")
            
            # Show statistics
            stats = api.get_statistics()
            if stats['status'] == 'success':
                total = stats['statistics']['total_law_changes']
                print(f"\nTotal law changes in database: {total}")
                
        else:
            print(f"Processing failed: {result['message']}")
            
    except Exception as e:
        print(f"Error in quick processing: {e}")


def show_database_contents():
    """
    Show current contents of the law changes database
    """
    print("="*80)
    print("DATABASE CONTENTS VIEWER")
    print("="*80)
    
    try:
        api = LawChangesAPI()
        
        # Get statistics
        stats = api.get_statistics()
        if stats['status'] == 'success':
            statistics = stats['statistics']
            print(f"📊 STATISTICS:")
            print(f"Total law changes: {statistics['total_law_changes']}")
            print(f"States with changes: {statistics['states_with_changes']}")
            
            if statistics['changes_by_state']:
                print(f"\nChanges by state:")
                for state, count in sorted(statistics['changes_by_state'].items(), 
                                         key=lambda x: x[1], reverse=True):
                    print(f"  • {state}: {count}")
        
        # Get recent changes
        recent = api.get_law_changes(limit=10)
        if recent['status'] == 'success' and recent['law_changes']:
            print(f"\n📚 RECENT LAW CHANGES:")
            print("-" * 80)
            for i, change in enumerate(recent['law_changes'], 1):
                print(f"{i}. Date: {change['date_changed']} | State: {change['state']}")
                summary = change['summary']
                if len(summary) > 100:
                    summary = summary[:97] + "..."
                print(f"   Summary: {summary}")
                print(f"   URL: {change['url']}")
                print(f"   PDF: {change['pdf_filename'] or 'N/A'}")
                print()
        else:
            print("\n📚 No law changes found in database")
            
        # Show database location
        print(f"💾 Database file: {api.db_service.db_path}")
        
    except Exception as e:
        print(f"Error accessing database: {e}")


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            quick_demo()
        elif sys.argv[1] == "--view-db":
            show_database_contents()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Available options:")
            print("  --quick     : Quick demo with sample PDF")
            print("  --view-db   : View current database contents")
    else:
        main()
        
        # Show available options
        print(f"\n💡 ADDITIONAL OPTIONS:")
        print(f"   python {os.path.basename(__file__)} --quick     # Quick demo")
        print(f"   python {os.path.basename(__file__)} --view-db   # View database")
