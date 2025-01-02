class File {
  public original_file: Blob
  public file_name: string

  public constructor(original_file: Blob, file_name: string) {
    this.original_file = original_file
    this.file_name = file_name
  }
}

export { File }