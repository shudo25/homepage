<!-- AI Context Standard v0.4 - Adopted: 2026-02-11 -->
# AI Assistant Initialization Guide

**Purpose**: Initialize AI context for working with this repository  
**Magic phrase**: "Please read COPILOT-INIT.md to initialize"

---

## 📚 Core Documents to Read

When starting a new session, read these files in order:

1. **README.md** - Repository overview
2. **This file (COPILOT-INIT.md)** - Working conventions
3. **PROJECT_STATUS.md** - Current work and recent history
4. **AI_CONTEXT_STANDARD.md** - The standard this repository follows (optional reference)

---

## 🎯 Repository Context

### What This Repository Is

This is the source repository for the **修道２５回生（Shudo 25th Class）website** and related AI assistant tools:

- **Primary purpose**: Website source for https://shudo25.github.io/homepage/
- **Secondary purpose**: AI assistant development (voice recognition, TTS, presentation generation)
- **Nature**: Mixed-purpose repository combining website content and development tools

### Key Components

```
docs/                    # Website content (GitHub Pages)
  ├── index.html        # Main landing page
  ├── events/           # Event information
  ├── meetings/         # Meeting minutes and info
  ├── groupinfo/        # Group information
  └── common/           # Shared CSS/JS resources

ai_codes/               # AI assistant v1 (older)
  ├── assistant-sasara.py        # Sasara voice assistant
  ├── zoom-agent-sasara.py       # Zoom integration
  └── characters/                # Character definitions

ai_v2/                  # AI assistant v2 (current development)
  ├── main_server.py             # Main server
  ├── tts_server.py              # Text-to-speech server
  ├── webui_server.py            # Web UI
  └── objects/                   # Core objects

present/                # Presentation generation tools
  ├── create_ci_presentation_v3_final.py  # Latest version
  └── *.txt                               # Script templates

codes/                  # Utility scripts
encrypt_pdf.py         # PDF encryption utility
encrypt_photos.py      # Photo encryption utility
```

---

## 🔑 Working Conventions

### 1. **Language Usage**

- **Website content (docs/)**: Japanese
  - Natural, conversational Japanese appropriate for community website
  - Avoid overly formal or stiff expressions
  - Target audience: 修道25回生（alumni born around 1957, graduated 1975）

- **Code and documentation**: 
  - Code comments: English or Japanese (either acceptable)
  - Technical documentation: Japanese preferred
  - This INIT file: Japanese to match repository context

### 2. **Website Editing Conventions**

- **Simplicity first**: Keep HTML clean and readable
- **Responsive design**: Test on mobile and desktop
- **Shared resources**: CSS/JS in `docs/common/`
- **Self-contained pages**: Each section can stand alone
- **SEO considerations**: Proper meta tags, structured data

### 3. **Python Code Conventions**

- **Python version**: 3.11+ preferred
- **Type hints**: Use where beneficial (not mandatory for scripts)
- **Virtual environment**: `.venv/` (Git-ignored)
- **Dependencies**: Document in requirements.txt or inline comments
- **Character encoding**: UTF-8 for all files

### 4. **AI Assistant Development Conventions**

- **Current version**: ai_v2/ is active development
- **Legacy code**: ai_codes/ maintained but not primary focus
- **Character definition**: Sasara character in `characters/` modules
- **Server architecture**: Separate TTS server and main server
- **Testing**: Manual testing typical (no formal test suite yet)

### 5. **File Naming Conventions**

- **Website files**: Descriptive English names (e.g., `index.html`, `events.html`)
- **Scripts**: Descriptive names with underscores (e.g., `create_ci_presentation_v3_final.py`)
- **Documentation**: Markdown preferred (`.md`)
- **Data files**: JSON for structured data, TXT for simple lists

### 6. **Version Management**

- **No semantic versioning**: Files use v2, v3, etc. in names when needed
- **"Final" suffix**: Indicates stable version (e.g., `_v3_final.py`)
- **Git history**: Primary source of version tracking

### 7. **Failure Recovery Protocol** (AI Context Standard)

When you fail the same operation 3+ times:

1. **Stop the failing approach**
2. **Explain what you tried and why it's failing**
3. **Propose alternatives**:
   - Manual operation (user does it directly)
   - Different tool or approach
   - Accepting current state if acceptable
4. **Don't silently struggle** through 15+ failed attempts

**Applies to**:
- Large-scale file editing (100+ line deletions/insertions)
- Repeated tool failures
- Non-essential tasks where manual operation might be faster

---

## 📂 Directory-Specific Guidelines

### `docs/` - Website Content

**Structure**:
- One HTML file per major section
- Shared resources in `common/`
- Links use relative paths

**When editing**:
- Preserve existing CSS class patterns
- Maintain responsive.css compatibility
- Check wrap-toggle.js integration
- Test on mobile layout

**Style guidelines**:
- Use semantic HTML5 elements
- Keep inline styles minimal
- Color-coded sections per content type
- Consistent navigation structure

### `ai_v2/` - Current AI Development

**Entry points**:
- `main_server.py` - Main assistant server
- `tts_server.py` - Text-to-speech service
- `webui_server.py` - Web interface
- `assistant_cli.py` - Command-line interface

**Key concepts**:
- Separate TTS from main logic
- Character-based voice selection
- WebSocket for real-time communication

### `present/` - Presentation Tools

**Latest version**: `create_ci_presentation_v3_final.py`

**Input files** (TXT format):
- Script: `ci_presentation_script_v3.txt`
- Slides: `ci_presentation_slides_v3.txt`
- Manual: `ci_presentation_manual_guide.txt`

**Output**: PowerPoint files (`.pptx`)

---

## 💡 Quick Tips for AI Assistants

### When Working on Website

1. **Preview changes**: Suggest viewing in browser after edits
2. **Check responsiveness**: Consider mobile layout
3. **Preserve structure**: Don't accidentally break navigation
4. **Japanese text**: Ensure natural phrasing

### When Working on AI Code

1. **Check ai_v2/ first**: Current development location
2. **Character context**: Sasara is the primary character
3. **Server dependencies**: TTS server must run separately
4. **Audio routing**: Voicemeeter configuration documented

### When Working on Presentations

1. **Use latest version**: v3_final is current
2. **Script format**: Specific TXT format expected
3. **Slide structure**: Hierarchical outline format
4. **PowerPoint library**: Uses python-pptx

### General Tips

1. **Read PROJECT_STATUS.md** for current focus
2. **Check workspace structure** before large changes
3. **Ask before major restructuring**
4. **Propose alternatives** for ambiguous requests
5. **Stop after 3 failures** and explain situation

---

## 🎯 Common Tasks

### Website Updates

```bash
# Edit HTML in docs/
# Preview locally (open in browser)
# Commit and push (GitHub Pages auto-deploys)
```

### AI Assistant Development

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows

# Run TTS server
python ai_v2/tts_server.py

# Run main server (separate terminal)
python ai_v2/main_server.py
```

### Presentation Generation

```bash
# Edit script and slides TXT files
# Run generator
python present/create_ci_presentation_v3_final.py
```

---

## ⚠️ Important Notes

### Sensitive Files

- `.env` - Environment variables (Git-ignored)
- `encrypt_pdf.py`, `encrypt_photos.py` - Handle carefully

### External Dependencies

- **CeVIO AI** - For TTS (Windows application)
- **Voicemeeter** - Audio routing (documented in docs/)
- **PowerPoint/LibreOffice** - For presentation output

### Performance Considerations

- Large file operations: Use appropriate tools
- Website: Keep images optimized
- AI models: Stored in `ai_codes/models/` (Git-ignored)

---

## 🔗 Related Resources

- **Website**: https://shudo25.github.io/homepage/
- **AI Context Standard**: See AI_CONTEXT_STANDARD.md in this repo
- **Character specs**: See `ai_codes/webui_sasara_spec.md`

---

**Last updated**: 2026-02-11  
**Standard version**: v0.4
