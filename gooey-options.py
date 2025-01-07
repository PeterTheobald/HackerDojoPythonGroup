from gooey import Gooey, GooeyParser

@Gooey(
    program_name="Dataset Processor",
    program_description="Process datasets with various options.",
    default_size=(800, 600),
    tabbed_groups=True,  # Organize arguments in tabs
    optional_cols=2      # Display optional arguments in two columns
)
def main():
    # Create argument parser
    parser = GooeyParser(description="Process datasets with a variety of options.")

    # File arguments
    file_group = parser.add_argument_group("File Options")
    file_group.add_argument("--input", metavar="Input File", help="Path to the input dataset", widget="FileChooser")
    file_group.add_argument("--output", metavar="Output File", help="Path to save the processed dataset", widget="FileSaver")

    # Processing arguments
    process_group = parser.add_argument_group("Processing Options")
    process_group.add_argument("--columns", metavar="Columns", help="Columns to process (comma-separated)")
    process_group.add_argument("--filter", metavar="Filter", help="Filter criteria (e.g., 'age>30')")
    process_group.add_argument("--sort", metavar="Sort By", help="Column to sort by")

    # Advanced options
    advanced_group = parser.add_argument_group("Advanced Options")
    advanced_group.add_argument("--normalize", action="store_true", help="Normalize the data")
    advanced_group.add_argument("--fill-missing", metavar="Fill Missing Values", help="Method to handle missing values (e.g., mean, median)")
    advanced_group.add_argument("--encoding", metavar="Encoding", help="File encoding", default="utf-8")
    advanced_group.add_argument("--verbose", action="store_true", help="Enable verbose mode")

    # Execution options
    execution_group = parser.add_argument_group("Execution Options")
    execution_group.add_argument("--threads", metavar="Threads", type=int, default=1, help="Number of threads to use")
    execution_group.add_argument("--timeout", metavar="Timeout", type=int, help="Timeout in seconds")
    execution_group.add_argument("--dry-run", action="store_true", help="Run without saving changes")

    # Parse arguments
    args = parser.parse_args()

    # Display parsed arguments
    print("Arguments received:")
    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")
    print(f"Columns: {args.columns}")
    print(f"Filter: {args.filter}")
    print(f"Sort: {args.sort}")
    print(f"Normalize: {args.normalize}")
    print(f"Fill Missing: {args.fill_missing}")
    print(f"Encoding: {args.encoding}")
    print(f"Verbose: {args.verbose}")
    print(f"Threads: {args.threads}")
    print(f"Timeout: {args.timeout}")
    print(f"Dry run: {args.dry_run}")

if __name__ == "__main__":
    main()

