# Aider

## 使用Aider
python -m pip install aider-install
aider-install

cd /to/your/project

export OPENAI_API_BASE={}
export OPENAI_API_KEY={}

aider --model openai/{}



## 安装magicskills

首先 `git clone https://github.com/Narwhal-Lab/MagicSkills.git`

并执行  `pip install -e .` 指令
或者直接`pip install magicskills` 

本文的示例 skill 以 **`docx`** 为例
### 安装 skill(之前已经下载过的可以选择跳过)

执行 `magicskills install skill_template  -t ~/allskills`


### 创建skills

执行 `magicskills createskills Aider_skills --skill-list c_2_ast --agent-md-path ./AGENTS.md`

### 生成 AGETNS.md

执行 `magicskills syncskills Aider_skills --mode cli_description --output ./AGENTS.md -y` 指定输出AGENTS.md路径，不指定时候就默认用`createskills`指定的`--agent-md-path ./AGENTS.md`
此时AGENTS.md会出现如下内容

```markdown
# AGENTS

<skills_system priority="1">

<!-- SKILLS_TABLE_START -->
<usage>
Unified skill CLI tool. Use "magicskills skill-tool listskill --name Aider_skills" to find relevant skills.
Then use "magicskills skill-tool readskill --arg <path>" to read the selected skill's SKILL.md or related docs.
If needed, use "magicskills skill-tool execskill --arg <command>" to run the command.
</usage>
<!-- SKILLS_TABLE_END -->

</skills_system>

```



# 了解更多AST知识

```bash
Readonly: Aider_example/AGENTS.md                                                               
> /run magicskills skill-tool listskill --name Aider_skills                                     

{
  "ok": true,
  "action": "listskill",
  "result": "1. name: c_2_ast\n   description: Parse C source code into an Abstract Syntax Tree (AST). Use when analyzing C programs, understanding code structure, performing static analysis, or preparing code for further program analysis (e.g., CFG, DFG, vulnerability detection).\n   path: /root/allskills/c_2_ast/SKILL.md"
}
Add 0.1k tokens of command output to the chat? (Y)es/(N)o [Yes]: y                              
Added 5 lines of output to the chat.
────────────────────────────────────────────────────────────────────────────────────────────────
Readonly: Aider_example/AGENTS.md                                                               
> /run magicskills skill-tool readskill /root/allskills/c_2_ast/SKILL.md                        

usage: magicskills [-h]
                   {listskill,readskill,execskill,syncskills,install,createskill,createskill_template,uploadskill,deleteskill,showskill,createskills,listskills,loadskills,deleteskills,saveskills,changetooldescription,changeclidescription,skill-tool} ...
magicskills: error: unrecognized arguments: /root/allskills/c_2_ast/SKILL.md
Add 0.1k tokens of command output to the chat? (Y)es/(N)o [Yes]: n                              
────────────────────────────────────────────────────────────────────────────────────────────────
Readonly: Aider_example/AGENTS.md                                                               
> /run magicskills skill-tool readskill --arg /root/allskills/c_2_ast/SKILL.md                  

{
  "ok": true,
  "action": "readskill",
  "result": "---\nname: c-to-ast\ndescription: Parse C source code into an Abstract Syntax Tree (AST). Use when analyzing C programs, understanding code structure, performing static analysis, or preparing code for further program analysis (e.g., CFG, DFG, vulnerability detection).\n---\n\n# C to AST Skill\n\n## Purpose\n\nThis Skill converts **C source code** into its **Abstract Syntax Tree (AST)** representation.\n\nUse this Skill when you need to:\n- Understand the structure of a C program\n- Analyze functions, statements, and expressions\n- Prepare C code for static analysis or security analysis\n- Transform C code into an intermediate representation (AST)\n- Feed structured code information into downstream tools or agents\n\nThe AST is generated using a Python-based C parser and printed directly to standard output.\n\n---\n\n## When to Use\n\nApply this Skill when the user asks to:\n- “Parse this C code”\n- “Convert this C file to an AST”\n- “Show me the AST of this C program”\n- “Analyze the structure of this C code”\n- “Extract syntax tree / abstract syntax tree from C”\n\nThis Skill is especially useful in **compiler frontends**, **program analysis**, and **security research** workflows.\n\n---\n\n## Instructions\n\nFollow these steps strictly and in order:\n\n1. **Navigate to the Skill scripts directory**\n   - Change working directory to:\n     ```\n     skills_for_all_agent/skill/c_2_ast/scripts/\n     ```\n\n2. **Handle the input C source**\n   - If the user provides a **path to a `.c` file**, use it directly.\n   - If the user provides **inline C code as a string**, you must first save it to a C source file using the provided script:\n     ```bash\n     python3 save_c.py --input \"<C code string>\" --output <output_dir> --filename <filename>.c\n     ```\n   - Ensure the generated file has a `.c` extension and is successfully written to disk.\n\n3. **Run the AST extraction script**\n   - Convert the C source file to its Abstract Syntax Tree by executing:\n     ```bash\n     python3 c_2_ast.py --input <path_to_c_file>\n     ```\n\n4. **Do not modify the source code**\n   - This Skill is strictly read-only.\n   - Do not rewrite, reformat, optimize, or otherwise alter the C code.\n\n5. **Return the AST output verbatim**\n   - The script prints the AST directly to standard output.\n   - Return the output exactly as produced.\n   - Do not summarize, paraphrase, or restructure the AST.\n   - Preserve indentation, hierarchy, and node ordering.\n\n6. **If parsing fails**\n   - Report the exact error message produced by the script.\n   - Suggest likely causes, such as:\n     - Missing or unsupported header files\n     - Unsupported C extensions (e.g., compiler-specific syntax)\n     - Invalid or incomplete C syntax\n\n---\n\n## Output Format\n\nThe output is a **tree-structured textual AST**, for example:\n\n````\n\nFileAST:\nFuncDef:\nDecl: main\nFuncDecl:\nTypeDecl:\nIdentifierType: ['int']\nCompound:\nFuncCall:\nID: puts\nExprList:\nConstant: string, \"Hello\"\nReturn:\nConstant: int, 0\n\n````\n\nThis output represents the syntactic structure of the C program and can be consumed by downstream tools.\n\n---\n\n## Additional Resources\n\nFor deeper understanding of:\n- AST node types\n- `pycparser` internal representation\n- Meaning of specific syntax tree nodes\n- Limitations of the C grammar supported\n\nsee the accompanying reference document:\n\n➡️ **[reference.md](reference.md)**\n\nOnly read this file **when more detailed or theoretical information is required**.  \nFor standard AST extraction tasks, this Skill file alone is sufficient.\n\n---\n\n## Notes and Limitations\n\n- The AST follows standard C syntax (C89/C99 subset).\n- Some compiler-specific extensions (e.g., GCC attributes) may not be supported.\n- Header files are handled using a minimal fake libc environment.\n- Macro-heavy or highly platform-specific code may require preprocessing.\n\n---\n\n## Examples\n\n### Example 1: Simple AST extraction\n\nUser request:\n> Convert this C file to an AST.\n\nAction:\n```bash\npython3 c_2_AST.py --input example.c\n````\n\nResult:\n\n* The AST is printed directly.\n\n---\n\n### Example 2: Security analysis preparation\n\nUser request:\n\n> I want to analyze this C program for vulnerabilities.\n\nAction:\n\n* First, extract the AST using this Skill.\n* Then, pass the AST to a vulnerability analysis or pattern-matching process.\n\n---\n\n## Best Practices\n\n* Use this Skill **before** any deep code analysis.\n* Treat the AST as an intermediate representation.\n* Combine with CFG/DFG or semantic analysis for advanced tasks.\n\n---\n\nEnd of Skill.\n"
}
Add 1.2k tokens of command output to the chat? (Y)es/(N)o [Yes]: y                              
Added 5 lines of output to the chat.
────────────────────────────────────────────────────────────────────────────────────────────────
Readonly: Aider_example/AGENTS.md                                                               
> /run magicskills skill-tool readskill --arg /root/allskills/c_2_ast/reference.md              

{
  "ok": true,
  "action": "readskill",
  "result": "# reference.md\n\n## C Abstract Syntax Tree (AST) Reference\n\nThis document provides **detailed reference material** for understanding the **Abstract Syntax Tree (AST)** generated from C source code by the `c_2_AST.py` script.\n\nRead this file **only when deeper knowledge is required**, such as:\n\n* Interpreting specific AST node types\n* Writing AST-based analyses or transformations\n* Performing vulnerability detection or code pattern matching\n* Mapping syntax to semantic structures (CFG / DFG)\n\n---\n\n## 1. What Is a C AST?\n\nAn **Abstract Syntax Tree (AST)** is a hierarchical representation of a program’s syntactic structure.\n\nKey properties:\n\n* Represents **syntax**, not runtime behavior\n* Ignores formatting, comments, and whitespace\n* Encodes structure: declarations, statements, expressions\n\nASTs are commonly used in:\n\n* Compilers and interpreters\n* Static analysis tools\n* Security auditing and vulnerability detection\n* Program understanding and refactoring tools\n\n---\n\n## 2. AST Format Used in This Skill\n\nThis Skill uses **`pycparser`**, a pure-Python C parser that supports a large subset of ISO C.\n\nThe AST is represented as a tree of Python objects, printed in a readable textual format using:\n\n```python\nast.show()\n```\n\nThe root node is always:\n\n```\nFileAST\n```\n\n---\n\n## 3. High-Level AST Structure\n\n```\nFileAST\n ├── Decl\n ├── FuncDef\n │    ├── Decl\n │    ├── ParamList\n │    └── Compound\n └── ...\n```\n\n* `FileAST`: Entire translation unit\n* Each child corresponds to a **top-level declaration or definition**\n\n---\n\n## 4. Core Node Types (Most Important)\n\n### 4.1 FileAST\n\n**Root node** of the AST.\n\n```text\nFileAST:\n  ext[0]: FuncDef\n  ext[1]: Decl\n```\n\nContains:\n\n* Global variable declarations\n* Function definitions\n* Type definitions\n\n---\n\n### 4.2 FuncDef (Function Definition)\n\nRepresents a full function definition.\n\n```text\nFuncDef:\n  Decl: main\n  ParamList\n  Compound\n```\n\nComponents:\n\n* `Decl`: function signature\n* `ParamList`: parameters (may be empty)\n* `Compound`: function body\n\n---\n\n### 4.3 Decl (Declaration)\n\nUsed for:\n\n* Variables\n* Functions\n* Parameters\n\n```text\nDecl: x\n  TypeDecl\n  Constant\n```\n\nKey attributes:\n\n* `name`: identifier\n* `type`: declared type\n* `init`: initializer (if any)\n\n---\n\n### 4.4 Type Nodes\n\nType information is represented hierarchically.\n\n#### TypeDecl\n\n```text\nTypeDecl:\n  IdentifierType: ['int']\n```\n\n#### PtrDecl\n\n```text\nPtrDecl:\n  TypeDecl\n```\n\n#### ArrayDecl\n\n```text\nArrayDecl:\n  TypeDecl\n  Constant\n```\n\n---\n\n### 4.5 Compound (Block)\n\nRepresents a `{ ... }` block.\n\n```text\nCompound:\n  Decl\n  Assignment\n  Return\n```\n\nUsed for:\n\n* Function bodies\n* Control-flow blocks\n\n---\n\n## 5. Statement Nodes\n\n### 5.1 Assignment\n\n```text\nAssignment:\n  ID: x\n  BinaryOp: +\n```\n\nRepresents:\n\n```c\nx = a + b;\n```\n\n---\n\n### 5.2 Return\n\n```text\nReturn:\n  Constant: int, 0\n```\n\nRepresents:\n\n```c\nreturn 0;\n```\n\n---\n\n### 5.3 If\n\n```text\nIf:\n  BinaryOp\n  Compound\n  Compound\n```\n\nRepresents:\n\n```c\nif (cond) { ... } else { ... }\n```\n\n---\n\n### 5.4 While / For\n\n```text\nWhile:\n  BinaryOp\n  Compound\n```\n\n```text\nFor:\n  Assignment\n  BinaryOp\n  Assignment\n  Compound\n```\n\n---\n\n## 6. Expression Nodes\n\n### 6.1 ID\n\n```text\nID: x\n```\n\nVariable reference.\n\n---\n\n### 6.2 Constant\n\n```text\nConstant: int, 42\nConstant: string, \"hello\"\n```\n\nLiteral values.\n\n---\n\n### 6.3 BinaryOp\n\n```text\nBinaryOp: +\n  ID: a\n  ID: b\n```\n\nRepresents:\n\n```c\na + b\n```\n\nOperators include:\n`+ - * / % < > == != && ||`\n\n---\n\n### 6.4 FuncCall\n\n```text\nFuncCall:\n  ID: puts\n  ExprList\n```\n\nRepresents:\n\n```c\nputs(\"hello\");\n```\n\n---\n\n## 7. Common Patterns (Analysis-Oriented)\n\n### Function Call Detection\n\nLook for:\n\n```\nFuncCall → ID(name)\n```\n\nUseful for:\n\n* Detecting dangerous functions (`gets`, `strcpy`)\n* API usage analysis\n\n---\n\n### Control Flow Detection\n\nLook for:\n\n* `If`\n* `For`\n* `While`\n* `Switch`\n\nThese nodes form the basis of **CFG construction**.\n\n---\n\n### Memory-Related Operations\n\nRelevant nodes:\n\n* `FuncCall` to `malloc`, `free`\n* Pointer `PtrDecl`\n* Dereference via `UnaryOp: *`\n\n---\n\n## 8. Limitations and Caveats\n\n* Supports **standard C**, not full GCC extensions\n* Macro-heavy code may be simplified by preprocessing\n* No semantic analysis (types are syntactic, not resolved)\n* No symbol resolution across files\n\nFor complex builds, preprocessing quality matters.\n\n---\n\n## 9. Typical Downstream Uses\n\nASTs extracted by this Skill are commonly used for:\n\n* Building **Control Flow Graphs (CFG)**\n* Extracting **Data Flow Graphs (DFG)**\n* Pattern-based vulnerability detection\n* Code similarity and embedding\n* Automated refactoring and transformation\n\n---\n\n## 10. Summary\n\n* AST = **structured syntax representation**\n* `FileAST` is always the root\n* Nodes map closely to C language constructs\n* Ideal intermediate form for static analysis and security research\n\nUse this reference as a **lookup guide**, not as required reading for every task.\n\n---\n\nEnd of reference.\n"
}
Add 1.6k tokens of command output to the chat? (Y)es/(N)o [Yes]: y                              
Added 5 lines of output to the chat.
────────────────────────────────────────────────────────────────────────────────────────────────
Readonly: Aider_example/AGENTS.md                                                               
> 请告诉我更多 AST 知识                                                                         

Based on your request to "tell me more AST knowledge", this is a request for educational content
rather than code changes. Since you've shared existing AST documentation (SKILL.md and          
reference.md from the c_2_ast skill), I'll create a new comprehensive AST reference file that   
expands on those materials.                                                                     

I'll create a new file docs/ast_comprehensive_guide.md with deeper AST knowledge covering       
multiple languages, advanced concepts, and practical applications.                              

docs/ast_comprehensive_guide.md                                                                 

                                                                                                
# Comprehensive Abstract Syntax Tree (AST) Guide                                                
                                                                                                
                                                                                                
                                                                                                
## Table of Contents                                                                            
                                                                                                
1. [Core Concepts](#core-concepts)                                                              
                                                                                                
2. [AST vs Parse Tree](#ast-vs-parse-tree)                                                      
                                                                                                
3. [Language-Specific ASTs](#language-specific-asts)                                            
                                                                                                
4. [Advanced AST Applications](#advanced-ast-applications)                                      
                                                                                                
5. [AST Manipulation Techniques](#ast-manipulation-techniques)                                  
                                                                                                
6. [Practical Analysis Patterns](#practical-analysis-patterns)                                  
                                                                                                
7. [Limitations and Challenges](#limitations-and-challenges)                                    
                                                                                                
                                                                                                
                                                                                                
---                                                                                             
                                                                                                
                                                                                                
                                                                                                
## Core Concepts                                                                                
                                                                                                
                                                                                                
                                                                                                
### What is an AST?                                                                             
                                                                                                
An **Abstract Syntax Tree (AST)** is a tree representation of source code's syntactic structure 
where:                                                                                          
                                                                                                
- Each node represents a construct in the source language                                       
                                                                                                
- Internal nodes represent operators or control structures                                      
                                                                                                
- Leaf nodes represent operands (identifiers, literals)                                         
                                                                                                
- Irrelevant details (whitespace, comments, parentheses) are omitted                            
                                                                                                
                                                                                                
                                                                                                
### Key Properties                                                                              
                                                                                                
1. **Hierarchical**: Parent-child relationships show containment                                
                                                                                                
2. **Lossy**: Doesn't preserve all source code details (e.g., formatting)                       
                                                                                                
3. **Language-Specific**: Structure depends on the grammar of the source language               
                                                                                                
4. **Intermediate Representation**: Bridges raw text and executable code                        
                                                                                                
                                                                                                
                                                                                                
### Basic AST Components                                                                        
                                                                                                
| Component       | Description                          | Example (C)                     |    
                                                                                                
|-----------------|--------------------------------------|---------------------------------|    
                                                                                                
| Root Node       | Top-level container                  | `FileAST`                       |    
                                                                                                
| Declaration     | Variable/function declarations       | `Decl`, `FuncDef`               |    
                                                                                                
| Statement       | Executable instructions              | `Assignment`, `If`, `Return`    |    
                                                                                                
| Expression      | Value-producing computations         | `BinaryOp`, `FuncCall`, `ID`    |    
                                                                                                
| Type            | Data type specifications             | `TypeDecl`, `PtrDecl`           |    
                                                                                                
                                                                                                
                                                                                                
---                                                                                             
                                                                                                
                                                                                                
                                                                                                
## AST vs Parse Tree                                                                            
                                                                                                
                                                                                                
                                                                                                
| Feature          | Parse Tree (Concrete Syntax Tree)       | Abstract Syntax Tree (AST)       
|                                                                                               
                                                                                                
|------------------|-----------------------------------------|----------------------------------
-|                                                                                              
                                                                                                
| **Detail Level** | Contains all grammar rules              | Omits syntactic noise            
|                                                                                               
                                                                                                
| **Structure**    | Mirrors exact grammar productions       | Simplified, meaningful structure 
|                                                                                               
                                                                                                
| **Use Case**     | Parser implementation                   | Code analysis/transformation     
|                                                                                               
                                                                                                
| **Example**      | Includes `expr → expr + term` nodes     | Direct `BinaryOp(+)` node        
|                                                                                               
                                                                                                
                                                                                                
                                                                                                
**Parse Tree Example** (for `a + b`):                                                           
                                                                                                

expr                                                                                            

├── expr                                                                                        

│   └── term                                                                                    

│       └── factor                                                                              

│           └── ID: a                                                                           

├── +                                                                                           

└── term                                                                                        

                                                                                                
└── factor                                                                                      
                                                                                                
    └── ID: b                                                                                   
                                                                                                

                                                                                                
                                                                                                
                                                                                                
**AST Equivalent**:                                                                             
                                                                                                

BinaryOp: +                                                                                     

├── ID: a                                                                                       

└── ID: b                                                                                       

                                                                                                
                                                                                                
                                                                                                
---                                                                                             
                                                                                                
                                                                                                
                                                                                                
## Language-Specific ASTs                                                                       
                                                                                                
                                                                                                
                                                                                                
### C/C++ (pycparser/Clang)                                                                     
                                                                                                
- **Root**: `TranslationUnitDecl`                                                               
                                                                                                
- **Key Nodes**:                                                                                
                                                                                                
  - `FunctionDecl`: Function definitions                                                        
                                                                                                
  - `VarDecl`: Variable declarations                                                            
                                                                                                
  - `CallExpr`: Function calls                                                                  
                                                                                                
  - `BinaryOperator`: Arithmetic/logical ops                                                    
                                                                                                
- **Special Features**:                                                                         
                                                                                                
  - Template handling (C++)                                                                     
                                                                                                
  - Preprocessor directives (as special nodes)                                                  
                                                                                                
                                                                                                
                                                                                                
### Python (ast module)                                                                         
                                                                                                
- **Root**: `Module`                                                                            
                                                                                                
- **Key Nodes**:                                                                                
                                                                                                
  - `FunctionDef`: Function definitions                                                         
                                                                                                
  - `Assign`: Variable assignments                                                              
                                                                                                
  - `Call`: Function calls                                                                      
                                                                                                
  - `BinOp`: Binary operations                                                                  
                                                                                                
- **Special Features**:                                                                         
                                                                                                
  - Context-sensitive (load/store/del)                                                          
                                                                                                
  - Decorator support                                                                           
                                                                                                
                                                                                                
                                                                                                
### JavaScript (ESTree/Babel)                                                                   
                                                                                                
- **Root**: `Program`                                                                           
                                                                                                
- **Key Nodes**:                                                                                
                                                                                                
  - `FunctionDeclaration`: Named functions                                                      
                                                                                                
  - `VariableDeclaration`: `var`/`let`/`const`                                                  
                                                                                                
  - `CallExpression`: Function calls                                                            
                                                                                                
  - `BinaryExpression`: Operations                                                              
                                                                                                
- **Special Features**:                                                                         
                                                                                                
  - JSX elements (in Babel)                                                                     
                                                                                                
  - Async/await syntax                                                                          
                                                                                                
                                                                                                
                                                                                                
### Java (Eclipse JDT/JavaParser)                                                               
                                                                                                
- **Root**: `CompilationUnit`                                                                   
                                                                                                
- **Key Nodes**:                                                                                
                                                                                                
  - `MethodDeclaration`: Methods                                                                
                                                                                                
  - `VariableDeclarationExpr`: Variables                                                        
                                                                                                
  - `MethodCallExpr`: Method invocations                                                        
                                                                                                
  - `BinaryExpr`: Operations                                                                    
                                                                                                
- **Special Features**:                                                                         
                                                                                                
  - Generics handling                                                                           
                                                                                                
  - Annotations                                                                                 
                                                                                                
                                                                                                
                                                                                                
---                                                                                             
                                                                                                
                                                                                                
                                                                                                
## Advanced AST Applications                                                                    
                                                                                                
                                                                                                
                                                                                                
### 1. Static Analysis                                                                          
                                                                                                
- **Taint Analysis**: Track data flow from sources to sinks                                     
                                                                                                
- **Control Flow Graph (CFG)**: Build execution paths from AST                                  
                                                                                                
- **Data Flow Analysis**: Compute variable definitions/uses                                     
                                                                                                
- **Pattern Matching**: Detect code smells/vulnerabilities                                      
                                                                                                
                                                                                                
                                                                                                
### 2. Program Transformation                                                                   
                                                                                                
- **Refactoring**: Rename variables, extract methods                                            
                                                                                                
- **Optimization**: Constant folding, dead code elimination                                     
                                                                                                
- **Transpilation**: Convert between language versions                                          
                                                                                                
- **Instrumentation**: Add logging/profiling code                                               
                                                                                                
                                                                                                
                                                                                                
### 3. Semantic Analysis                                                                        
                                                                                                
- **Type Checking**: Verify type compatibility                                                  
                                                                                                
- **Symbol Resolution**: Link identifiers to declarations                                       
                                                                                                
- **Scope Analysis**: Determine variable visibility                                             
                                                                                                
                                                                                                
                                                                                                
### 4. Security Applications                                                                    
                                                                                                
- **Vulnerability Detection**: Find buffer overflows, SQLi                                      
                                                                                                
- **Compliance Checking**: Enforce coding standards                                             
                                                                                                
- **Malware Analysis**: Identify suspicious patterns                                            
                                                                                                
                                                                                                
                                                                                                
---                                                                                             
                                                                                                
                                                                                                
                                                                                                
## AST Manipulation Techniques                                                                  
                                                                                                
                                                                                                
                                                                                                
### Traversal Strategies                                                                        
                                                                                                
1. **Depth-First Search (DFS)**:                                                                
                                                                                                
   ```python                                                                                    
                                                                                                
   def visit(node):                                                                             
                                                                                                
       process(node)                                                                            
                                                                                                
       for child in node.children:                                                              
                                                                                                
           visit(child)                                                                         
                                                                                                

 2 Breadth-First Search (BFS):                                                                  
                                                                                                
                                                                                                
   from collections import deque                                                                
                                                                                                
   queue = deque([root])                                                                        
                                                                                                
   while queue:                                                                                 
                                                                                                
       node = queue.popleft()                                                                   
                                                                                                
       process(node)                                                                            
                                                                                                
       queue.extend(node.children)                                                              
                                                                                                
 3 Visitor Pattern:                                                                             
                                                                                                
                                                                                                
   class ASTVisitor:                                                                            
                                                                                                
       def visit_BinaryOp(self, node):                                                          
                                                                                                
           # Handle binary operations                                                           
                                                                                                
           pass                                                                                 
                                                                                                
                                                                                                
                                                                                                
       def visit_Call(self, node):                                                              
                                                                                                
           # Handle function calls                                                              
                                                                                                
           pass                                                                                 
                                                                                                

Common Transformations                                                                          

| Operation          | Description                          | Example                          |

|--------------------|--------------------------------------|----------------------------------|

| Node Replacement | Substitute one node for another      | Replace x*2 with x<<1        |      

| Node Insertion  | Add new nodes                        | Insert logging before function   |   

| Node Deletion   | Remove nodes                         | Eliminate dead code              |   

| Attribute Update| Modify node properties               | Change variable name             |   

Serialization Formats                                                                           

 • JSON: Human-readable, language-agnostic                                                      
 • Protocol Buffers: Efficient binary format                                                    
 • S-Expressions: Lisp-style nested lists                                                       
 • Custom Text: Indented tree representations                                                   

------------------------------------------------------------------------------------------------


Practical Analysis Patterns                                                                     

1. Function Call Analysis                                                                       

Goal: Find all calls to dangerous functions                                                     

                                                                                                
def find_dangerous_calls(node):                                                                 
                                                                                                
    if isinstance(node, FuncCall) and node.name.name in ['gets', 'strcpy']:                     
                                                                                                
        report_vulnerability(node)                                                              
                                                                                                
    for child in node.children:                                                                 
                                                                                                
        find_dangerous_calls(child)                                                             
                                                                                                

2. Loop Detection                                                                               

Goal: Identify infinite loops                                                                   

                                                                                                
def check_infinite_loop(node):                                                                  
                                                                                                
    if isinstance(node, While) and node.cond == Constant('int', '1'):                           
                                                                                                
        return True                                                                             
                                                                                                
    # Check for missing break/continue in while(1)                                              
                                                                                                
    return False                                                                                
                                                                                                

3. Memory Safety                                                                                

Goal: Detect use-after-free                                                                     

                                                                                                
def track_memory(node, allocated=None, freed=None):                                             
                                                                                                
    if not allocated: allocated = set()                                                         
                                                                                                
    if not freed: freed = set()                                                                 
                                                                                                
                                                                                                
                                                                                                
    if is_malloc_call(node):                                                                    
                                                                                                
        var = get_return_var(node)                                                              
                                                                                                
        allocated.add(var)                                                                      
                                                                                                
    elif is_free_call(node):                                                                    
                                                                                                
        var = get_arg(node)                                                                     
                                                                                                
        freed.add(var)                                                                          
                                                                                                
        allocated.discard(var)                                                                  
                                                                                                
    elif is_use(node) and get_var(node) in freed:                                               
                                                                                                
        report_use_after_free(node)                                                             
                                                                                                

4. Complexity Metrics                                                                           

Goal: Calculate cyclomatic complexity                                                           

                                                                                                
def cyclomatic_complexity(node):                                                                
                                                                                                
    complexity = 1                                                                              
                                                                                                
    if isinstance(node, (If, For, While, Case)):                                                
                                                                                                
        complexity += 1                                                                         
                                                                                                
    for child in node.children:                                                                 
                                                                                                
        complexity += cyclomatic_complexity(child)                                              
                                                                                                
    return complexity                                                                           
                                                                                                

------------------------------------------------------------------------------------------------


Limitations and Challenges                                                                      

1. Language Coverage                                                                            

 • Problem: Parsers may not support all language features                                       
 • Example: GCC extensions in C, TypeScript decorators                                          
 • Solution: Preprocess code or use more complete parsers                                       

2. Context Sensitivity                                                                          

 • Problem: ASTs don't capture semantic context                                                 
 • Example: Overloaded functions, template instantiation                                        
 • Solution: Combine with symbol tables/type information                                        

3. Multi-file Analysis                                                                          

 • Problem: ASTs are typically per-file                                                         
 • Example: Cross-file function calls, include dependencies                                     
 • Solution: Build global symbol tables, use LSP                                                

4. Performance                                                                                  

 • Problem: Large codebases create huge ASTs                                                    
 • Example: Linux kernel has millions of AST nodes                                              
 • Solution: Incremental parsing, lazy loading                                                  

5. Error Recovery                                                                               

 • Problem: Invalid code breaks parsers                                                         
 • Example: Missing semicolons, unmatched braces                                                
 • Solution: Error-tolerant parsers (like in IDEs)                                              

------------------------------------------------------------------------------------------------


Recommended Tools by Language                                                                   

| Language   | Parser Library       | Visualization Tool     | Analysis Framework |             

|------------|----------------------|------------------------|--------------------|             

| C/C++      | Clang/LLVM           | AST Explorer           | CodeQL             |             

| Python     | ast (stdlib)         | Python Tutor           | LibCST             |             

| JavaScript | Babel/Esprima        | AST Explorer           | ESLint             |             

| Java       | JavaParser           | IntelliJ IDEA          | Soot               |             

| Go         | go/ast (stdlib)      | Go Playground          | go/analysis        |             

| Rust       | syn                  | Rust Analyzer          | rust-analyzer      |             

------------------------------------------------------------------------------------------------


Further Learning Resources                                                                      

 1 Books:                                                                                       
    • "Engineering a Compiler" by Keith Cooper                                                  
    • "Compilers: Principles, Techniques, and Tools" (Dragon Book)                              
 2 Online Tools:                                                                                
    • AST Explorer (multi-language)                                                             
    • Python AST Visualizer                                                                     
 3 Academic Papers:                                                                             
    • "Abstract Syntax and Variable Binding" (Harper et al.)                                    
    • "The AST Typing Problem" (Odersky)                                                        
 4 Practical Tutorials:                                                                         
    • LLVM Tutorial (Kaleidoscope)                                                              
    • Babel Plugin Handbook                                                                     
    • Python's ast module documentation                                                         

------------------------------------------------------------------------------------------------


▌ Key Insight: ASTs are the foundation of modern program analysis. Mastering them enables deep
▌ code understanding, transformation, and automation across all programming languages.        

                                                                                                
                                                                                                
                                                                                                


Tokens: 5.2k sent, 2.4k received.

docs/ast_comprehensive_guide.md

```

# 转换一段代码为AST代码

"Please help me convert the following C code into an AST.\n"
"```c\n"
"#include <stdio.h>\n\n"
"int main() {\n"
'    puts("Hello from agent");\n'
"    return 0;\n"
"}\n"
"```"

```bash
        Readonly: Aider_example/AGENTS.md                                                               
> /run magicskills skill-tool listskill --name Aider_skills                                     

{
  "ok": true,
  "action": "listskill",
  "result": "1. name: c_2_ast\n   description: Parse C source code into an Abstract Syntax Tree (AST). Use when analyzing C programs, understanding code structure, performing static analysis, or preparing code for further program analysis (e.g., CFG, DFG, vulnerability detection).\n   path: /root/allskills/c_2_ast/SKILL.md"
}
Add 0.1k tokens of command output to the chat? (Y)es/(N)o [Yes]: y                              
Added 5 lines of output to the chat.
────────────────────────────────────────────────────────────────────────────────────────────────
Readonly: Aider_example/AGENTS.md                                                               
> /run magicskills skill-tool readskill /root/allskills/c_2_ast/SKILL.md                        

usage: magicskills [-h]
                   {listskill,readskill,execskill,syncskills,install,createskill,createskill_template,uploadskill,deleteskill,showskill,createskills,listskills,loadskills,deleteskills,saveskills,changetooldescription,changeclidescription,skill-tool} ...
magicskills: error: unrecognized arguments: /root/allskills/c_2_ast/SKILL.md
Add 0.1k tokens of command output to the chat? (Y)es/(N)o [Yes]: n                              
────────────────────────────────────────────────────────────────────────────────────────────────
Readonly: Aider_example/AGENTS.md                                                               
> /run magicskills skill-tool readskill --arg /root/allskills/c_2_ast/SKILL.md                  

{
  "ok": true,
  "action": "readskill",
  "result": "---\nname: c-to-ast\ndescription: Parse C source code into an Abstract Syntax Tree (AST). Use when analyzing C programs, understanding code structure, performing static analysis, or preparing code for further program analysis (e.g., CFG, DFG, vulnerability detection).\n---\n\n# C to AST Skill\n\n## Purpose\n\nThis Skill converts **C source code** into its **Abstract Syntax Tree (AST)** representation.\n\nUse this Skill when you need to:\n- Understand the structure of a C program\n- Analyze functions, statements, and expressions\n- Prepare C code for static analysis or security analysis\n- Transform C code into an intermediate representation (AST)\n- Feed structured code information into downstream tools or agents\n\nThe AST is generated using a Python-based C parser and printed directly to standard output.\n\n---\n\n## When to Use\n\nApply this Skill when the user asks to:\n- “Parse this C code”\n- “Convert this C file to an AST”\n- “Show me the AST of this C program”\n- “Analyze the structure of this C code”\n- “Extract syntax tree / abstract syntax tree from C”\n\nThis Skill is especially useful in **compiler frontends**, **program analysis**, and **security research** workflows.\n\n---\n\n## Instructions\n\nFollow these steps strictly and in order:\n\n1. **Navigate to the Skill scripts directory**\n   - Change working directory to:\n     ```\n     skills_for_all_agent/skill/c_2_ast/scripts/\n     ```\n\n2. **Handle the input C source**\n   - If the user provides a **path to a `.c` file**, use it directly.\n   - If the user provides **inline C code as a string**, you must first save it to a C source file using the provided script:\n     ```bash\n     python3 save_c.py --input \"<C code string>\" --output <output_dir> --filename <filename>.c\n     ```\n   - Ensure the generated file has a `.c` extension and is successfully written to disk.\n\n3. **Run the AST extraction script**\n   - Convert the C source file to its Abstract Syntax Tree by executing:\n     ```bash\n     python3 c_2_ast.py --input <path_to_c_file>\n     ```\n\n4. **Do not modify the source code**\n   - This Skill is strictly read-only.\n   - Do not rewrite, reformat, optimize, or otherwise alter the C code.\n\n5. **Return the AST output verbatim**\n   - The script prints the AST directly to standard output.\n   - Return the output exactly as produced.\n   - Do not summarize, paraphrase, or restructure the AST.\n   - Preserve indentation, hierarchy, and node ordering.\n\n6. **If parsing fails**\n   - Report the exact error message produced by the script.\n   - Suggest likely causes, such as:\n     - Missing or unsupported header files\n     - Unsupported C extensions (e.g., compiler-specific syntax)\n     - Invalid or incomplete C syntax\n\n---\n\n## Output Format\n\nThe output is a **tree-structured textual AST**, for example:\n\n````\n\nFileAST:\nFuncDef:\nDecl: main\nFuncDecl:\nTypeDecl:\nIdentifierType: ['int']\nCompound:\nFuncCall:\nID: puts\nExprList:\nConstant: string, \"Hello\"\nReturn:\nConstant: int, 0\n\n````\n\nThis output represents the syntactic structure of the C program and can be consumed by downstream tools.\n\n---\n\n## Additional Resources\n\nFor deeper understanding of:\n- AST node types\n- `pycparser` internal representation\n- Meaning of specific syntax tree nodes\n- Limitations of the C grammar supported\n\nsee the accompanying reference document:\n\n➡️ **[reference.md](reference.md)**\n\nOnly read this file **when more detailed or theoretical information is required**.  \nFor standard AST extraction tasks, this Skill file alone is sufficient.\n\n---\n\n## Notes and Limitations\n\n- The AST follows standard C syntax (C89/C99 subset).\n- Some compiler-specific extensions (e.g., GCC attributes) may not be supported.\n- Header files are handled using a minimal fake libc environment.\n- Macro-heavy or highly platform-specific code may require preprocessing.\n\n---\n\n## Examples\n\n### Example 1: Simple AST extraction\n\nUser request:\n> Convert this C file to an AST.\n\nAction:\n```bash\npython3 c_2_AST.py --input example.c\n````\n\nResult:\n\n* The AST is printed directly.\n\n---\n\n### Example 2: Security analysis preparation\n\nUser request:\n\n> I want to analyze this C program for vulnerabilities.\n\nAction:\n\n* First, extract the AST using this Skill.\n* Then, pass the AST to a vulnerability analysis or pattern-matching process.\n\n---\n\n## Best Practices\n\n* Use this Skill **before** any deep code analysis.\n* Treat the AST as an intermediate representation.\n* Combine with CFG/DFG or semantic analysis for advanced tasks.\n\n---\n\nEnd of Skill.\n"
}
Add 1.2k tokens of command output to the chat? (Y)es/(N)o [Yes]: y                              
Added 5 lines of output to the chat.
────────────────────────────────────────────────────────────────────────────────────────────────
Readonly: Aider_example/AGENTS.md                                                                                             
> /run magicskills skill-tool execskill --arg "bash -lc \"cd /root/allskills/c_2_ast/scripts && python3 save_c.py --inpu
> t \$'#include <stdio.h>\\n\\nint main() {\\n    puts(\\\"Generated by agent\\\");\\n    return 0;\\n}\\n' --output /tm
> p/c2ast_demo --filename demo_once.c && python3 c_2_ast.py --input /tmp/c2ast_demo/demo_once.c\"" 
>                                                                                                                       

{
  "ok": true,
  "action": "execskill",
  "result": {
    "command": "bash -lc \"cd /root/allskills/c_2_ast/scripts && python3 save_c.py --input $'#include <stdio.h>\\n\\nint main() {\\n    puts(\\\"Generated by agent\\\");\\n    return 0;\\n}\\n' --output /tmp/c2ast_demo --filename demo_once.c && python3 c_2_ast.py --input /tmp/c2ast_demo/demo_once.c\"",
    "returncode": 0,
    "stdout": "[OK] C source saved to: /tmp/c2ast_demo/demo_once.c\nFileAST: \n  Typedef: FILE, [], ['typedef']\n    TypeDecl: FILE, [], None\n      IdentifierType: ['int']\n  Decl: printf, [], [], [], []\n    FuncDecl: \n      ParamList: \n        Decl: fmt, ['const'], [], [], []\n          PtrDecl: []\n            TypeDecl: fmt, ['const'], None\n              IdentifierType: ['char']\n        EllipsisParam: \n      TypeDecl: printf, [], None\n        IdentifierType: ['int']\n  Decl: puts, [], [], [], []\n    FuncDecl: \n      ParamList: \n        Decl: s, ['const'], [], [], []\n          PtrDecl: []\n            TypeDecl: s, ['const'], None\n              IdentifierType: ['char']\n      TypeDecl: puts, [], None\n        IdentifierType: ['int']\n  FuncDef: \n    Decl: main, [], [], [], []\n      FuncDecl: \n        TypeDecl: main, [], None\n          IdentifierType: ['int']\n    Compound: \n      FuncCall: \n        ID: puts\n        ExprList: \n          Constant: string, \"Generated by agent\"\n      Return: \n        Constant: int, 0\n",
    "stderr": ""
  }
}
```