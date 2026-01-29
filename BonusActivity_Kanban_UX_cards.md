# GitHub Projects - Kanban Workflow for GDM Chatbot

> **Goal:** Track UX research, database design, and development work using a Kanban board with simple task sizing.

---

## Quick Start

### 1. Create Your Project Board

1. Go to your repository → **Projects** tab
2. Click **New project**
3. Choose **Board** template
4. Name it: `GDM Chatbot Development`

**Default Columns:**
```
📋 Backlog  →  📝 To Do  →  🏗️ In Progress  →  ✅ Done
```

---

## Task Sizing: S / M / L

We use **T-shirt sizing** instead of story points - it's simpler and faster.

| Size | Time Estimate | Example Tasks |
|------|---------------|---------------|
| **S** (Small) | ~1-2 hours | • Review interview data<br>• Add 2-3 fields to database table<br>• Write 5 user stories |
| **M** (Medium) | ~3-5 hours | • Create 2 patient personas<br>• Design complete database table<br>• Build login form UI |
| **L** (Large) | ~1 day | • Design full database schema<br>• Implement glucose tracking feature<br>• Conduct user testing session |

**Rule:** If a task feels bigger than L, break it down into smaller tasks!

---

## Creating Cards - Template

### For UX Research

```markdown
**Title:** [M] Create Patient Personas

**Description:**
Build 2 distinct patient personas from interview data.

**Deliverable:**
- 2 completed persona worksheets
- One urban tech-savvy patient
- One rural low-literacy patient

**Done When:**
- Based on interview quotes
- Captures goals, pain points, tech comfort
- Reviewed by partner
```

### For Database Design

```markdown
**Title:** [M] Design Glucose Tracking Schema

**Description:**
Create table to store glucose readings per ADA guidelines (4+ readings/day).

**Deliverable:**
- `glucose_readings` table with fields
- Timestamps, reading types, meal context
- Flags for high/low readings

**Done When:**
- Supports all reading types (fasting, post-meal)
- Can query by date, patient, type
- Tested with sample data
```

### For Code Implementation

```markdown
**Title:** [L] Implement Patient Login

**Description:**
Build authentication system with profile types.

**Deliverable:**
- Login form (email/password)
- User registration
- Session management
- Role-based redirect (patient vs provider)

**Done When:**
- Users can register and log in
- Sessions persist
- Passwords are hashed
- Tests pass
```

---

## Example Board State

### This Week (After Lecture)

**📋 Backlog**
- [M] Design Provider Dashboard UI
- [M] Research Malayalam language support
- [S] Write Kerala diet content

**📝 To Do** ← Focus here this week
- [M] Complete 2 Patient Personas
- [M] Design Glucose Tracking Schema
- [S] Write 6 User Stories
- [M] Set up SQLite Database

**🏗️ In Progress**
- [M] Create Patient Personas (You're working on this!)

**✅ Done**
- [S] Read Interview Data
- [S] Set up Project Board

---

## Workflow Tips

### Moving Cards

Drag cards between columns as you work:

1. **Backlog** → Nice to have, not urgent
2. **To Do** → Committed this week
3. **In Progress** → Actively working (limit to 1-2 tasks!)
4. **Done** → Completed and reviewed

### Linking to Code

When you start coding:
```markdown
**Title:** [M] Implement Patient Login

**Related:**
- Branch: `feature/patient-login`
- PR: #12

**Progress:**
- ✅ Login form UI
- ✅ Database schema
- 🏗️ Password hashing
- ⬜ Session management
```

### Adding Details

Click any card to add:
- **Comments:** Updates, blockers, questions
- **Checklists:** Break task into sub-steps
- **Labels:** `database`, `ux`, `urgent`, `blocked`
- **Assignees:** Who's working on it

---

## Assignment for This Week

### After Today's Lecture, Add These Cards:

#### Card 1: Complete Personas
```
Title: [M] Finalize 2 Patient Personas
Description: Clean up personas from class activity
Done When: Typed up, includes all sections, partner-reviewed
```

#### Card 2: Database Schema
```
Title: [M] Implement SQLite Schema
Description: Create database with users, patients, glucose_readings tables
Done When: Database file created, tables exist, sample data inserted
```

#### Card 3: User Stories
```
Title: [S] Document User Stories
Description: Type up 6 user stories from class (3 per persona)
Done When: Added to repo README or docs/ folder
```

---

## Common Questions

**Q: Do I move cards myself or does it happen automatically?**  
A: You move them manually. (GitHub Actions can automate, but not required for now.)

**Q: What if I'm stuck on a task?**  
A: Add a comment on the card: "Blocked: Need help with X". Move to "To Do" and pick another task.

**Q: Should I create cards for reading documentation?**  
A: Only if it takes >1 hour. Small learning tasks don't need cards.

**Q: Can I change a task from M to L mid-work?**  
A: Yes! Update the title if you realize it's bigger than expected. Learn for next time.

---

## Visual Example

Here's what a card looks like when you click it:

```
┌─────────────────────────────────────────────┐
│ [M] Create Patient Personas           Edit  │
├─────────────────────────────────────────────┤
│                                              │
│ Build 2 distinct patient personas from      │
│ interview data.                             │
│                                              │
│ Deliverable:                                │
│ ☐ Persona 1: Urban tech-savvy              │
│ ☐ Persona 2: Rural low-literacy            │
│ ☐ Partner review completed                 │
│                                              │
│ Labels: 🏷️ ux  🏷️ research                 │
│                                              │
│ Comments:                                   │
│ You: "Working on this now"                 │
│ Partner: "Let's review together at 3pm"    │
└─────────────────────────────────────────────┘
```

---

## Next Steps

1. Create your board (5 min)
2. Add 3 cards for this week's work (10 min)
3. Move one card to "In Progress" (now!)
4. Update as you work

**Remember:** The board is a tool to help you, not a burden. Keep it simple!

---

## Resources

- [GitHub Projects Docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- Need help? Ask in Discord or office hours!