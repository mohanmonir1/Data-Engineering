# Markdown Details
Markdown is a lightweight markup language with plain text formatting syntax. It is designed to be easy to read and write, and it can be converted to HTML and other formats. Markdown is widely used for formatting readme files, writing messages in online discussion forums, and creating rich text using a plain text editor.

## Key Features of Markdown:
- **Simplicity**: Easy to learn and use.
- **Portability**: Can be used across different platforms and devices.
- **Flexibility**: Supports various formatting options like headings, lists, links, images, and more.

## Examples of Markdown Usage:
- **Readme Files**: Used in GitHub repositories to provide information about the project.
- **Documentation**: Used to create user manuals and guides.
- **Blogging**: Many blogging platforms support Markdown for writing posts.

# Normal Text
Write the text without any special characters.

# Line Break
Add 2 spaces at the end of the line, then press enter.  
Example:  
My Name is Mohan R.  
I am 23 years old.

# Paragraph
To add a line between two paragraphs, add an extra line between paragraphs.  
Example:

Paragraph1

Paragraph2

# Headings
# Heading 1
## Heading 2
### Heading 3
#### Heading 4

# Bold and Italic
**Bold**: To bold the text, use either double asterisks or double underscores.  
Example: **This is bold text** or __This is bold text__.

_Italic_: To italicize the text, use either a single asterisk or a single underscore.  
Example: *This is italic text* or _This is italic text_.

***Bold and Italic***: To apply both, use triple asterisks or triple underscores, or a combination of asterisks and underscores.  
Example: ***Bold and Italic***, ___Bold and Italic___, __*Bold and Italic*__, **_Bold and Italic_**.

# Strike Through
To strike through the text, use double tildes (~).  
Example: ~~This text is crossed out~~

# Highlight
To highlight the text, use double equal signs. In some markdowns, double equal signs will support or else use `<mark> </mark>`.  
Example: ==Highlight== : This one is not supported in VS preview.  
`<mark>Highlight</mark>`: This one is supported in VS preview. <mark>Highlight</mark>

# Superscript and Subscript
**Superscript**: To superscript the text, use a single ^. In some markdowns, a single ^ sign will support or else use `<sup> </sup>`.  
Example: a^2^: This one is not supported in VS preview.  
`a<sup>2</sup>`: This one is supported in VS preview. a<sup>2</sup>

__Subscript__: To subscript the text, use single ~. In some markdowns, single ~ signs will support or else use `<sub> </sub>`.  
Example: H~2~O: This one is not supported in VS preview.  
`H<sub>2</sub>O`: This one is supported in VS preview. H<sub>2</sub>O


# Code Blocks in Markdown

To create a code block, you can use **triple backticks** or **indent the code by four spaces**. Below are examples of both methods:

### Using Triple Backticks

```
def hello_world():
    print("Hello, world!")
```

### Specifying the Language

You can specify the language used in the code block by writing the language name after the triple backticks:

```python
def hello_world():
    print("Hello, world!")
```

### Using Indentation

Alternatively, you can create a code block by indenting the code by four spaces:

    def hello_world():
        print("Hello, world!")

# Links
To create a hyperlink, use square brackets followed by parentheses.  
Syntax: `[link text](link)`  
Example: [Markdown Tutorial Youtube Link](https://www.youtube.com/watch?v=_PPWWRV6gbA)

# Images
To add an image, use an exclamation mark followed by square brackets and parentheses.  
Syntax: `![image name]()`  
Example: ![Azure Databricks Logo](https://th.bing.com/th/id/OIP.zaZ-D5m1KdijBMWDNBx3VAHaIW?rs=1&pid=ImgDetMain)

# Add Line
To add line between sentence, use **triple asterisks** or **triple underscore**.  
Note: It is recomended to add extra line.  
Example1:  
This one is first paragraph

***

This one is second paragraph

Example2:  
This one is first paragraph

___

This one is second paragraph

# Lists
## Unordered Lists
To create an unordered list, use asterisks, plus signs, or hyphens.  
Example:  
- Item 1  
- Item 2  
- Item 3  

## Ordered Lists
To create an ordered list, use numbers followed by periods.  
Example:  
1. First item  
2. Second item  
3. Third item

## Nested Lists
To create a nested list, add 4 spaces
1. First item
    - First first item
    - First second item
2. Second item
3. Third item

# Creating Tables in Markdown

Tables in Markdown are created using pipes (`|`) and hyphens (`-`). Below are the steps and examples to help you create tables:

### Basic Table Structure

A simple table consists of a header row and one or more data rows. The columns are separated by pipes (`|`), and the header is separated from the body by hyphens (`-`).

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1, Col 1 | Row 1, Col 2 | Row 1, Col 3 |
| Row 2, Col 1 | Row 2, Col 2 | Row 2, Col 3 |
```

### Example

| Name       | Age | Occupation    |
|------------|-----|---------------|
| Alice      | 30  | Engineer      |
| Bob        | 25  | Designer      |
| Charlie    | 35  | Teacher       |

### Aligning Text

You can align text within columns by adding colons (`:`) to the hyphens:

- **Left-aligned**: `:---`
- **Center-aligned**: `:---:`
- **Right-aligned**: `---:`

```markdown
| Left Align | Center Align | Right Align |
|:-----------|:------------:|------------:|
| This       | is           | a test      |
| Markdown   | table        | example     |
```

### Example with Alignment
| Name       | Age | Occupation    |
|:-----------|:---:|--------------:|
| Alice      |  30 | Engineer      |
| Bob        |  25 | Designer      |
| Charlie    |  35 | Teacher       |

# Creating Checklists in Markdown

Checklists, also known as task lists, are a great way to keep track of tasks or items. You can create checklists using square brackets (`[ ]` for unchecked and `[x]` for checked) within a list.

### Basic Checklist Structure

To create a checklist, use the following syntax:

```markdown
- [ ] Task 1
- [ ] Task 2
- [x] Task 3 (completed)
```

### Example
**My To-Do List**
- [ ] Buy groceries
- [ ] Finish homework
- [x] Call mom
- [ ] Read a book

### Nested Checklists

You can also create nested checklists by indenting the items:

```markdown
- [ ] Task 1
    - [ ] Subtask 1.1
    - [x] Subtask 1.2 (completed)
- [ ] Task 2
    - [ ] Subtask 2.1
```

### Example with Nested Checklists

**Project Tasks**

- [ ] Design phase
    - [ ] Create wireframes
    - [x] Review designs (completed)
- [ ] Development phase
    - [ ] Set up environment
    - [ ] Write code
- [ ] Testing phase
    - [ ] Unit tests
    - [ ] Integration tests