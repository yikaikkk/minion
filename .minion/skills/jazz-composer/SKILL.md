---
name: jazz-composer
description: Compose original jazz music including chord progressions, melodies, and arrangements in various jazz styles (bebop, cool jazz, modal, hard bop, fusion, etc.). Use this skill whenever users ask for jazz composition, want to create jazz chord progressions, need help writing jazz melodies or solos, request jazz arrangements, or seek assistance with jazz theory applied to composition. This skill should be used for any jazz-related musical creation tasks, even if the user doesn't explicitly mention "composition" but clearly needs original jazz music content.
---

# Jazz Composer Skill

This skill enables Claude to compose original jazz music across various styles and formats. The skill provides comprehensive jazz composition capabilities including harmonic analysis, melodic development, rhythmic concepts, and arrangement techniques.

## Core Capabilities

### 1. Jazz Styles Coverage
- **Bebop**: Fast tempos, complex chord changes, virtuosic melodies
- **Cool Jazz**: Relaxed tempos, lighter tone, sophisticated harmonies  
- **Hard Bop**: Blues and gospel influences, soulful melodies
- **Modal Jazz**: Based on scales/modes rather than chord progressions
- **Fusion**: Combines jazz with rock, funk, or electronic elements
- **Swing**: Big band era style with strong rhythmic drive
- **Free Jazz**: Atonal, experimental approaches to improvisation

### 2. Composition Elements
- **Chord Progressions**: Create authentic jazz harmony using ii-V-I, tritone substitutions, modal interchange, etc.
- **Melodies**: Develop singable, jazz-appropriate melodic lines with proper phrasing
- **Rhythmic Concepts**: Incorporate swing feel, syncopation, polyrhythms
- **Arrangements**: Structure pieces with intros, heads, solos, backgrounds, and outros
- **Lead Sheets**: Generate complete lead sheets with melody, chords, and form

### 3. Output Formats
Always provide multiple output formats when possible:
- **Text Description**: Clear explanation of the musical content
- **Chord Chart**: Standard jazz notation showing chord symbols and form
- **ABC Notation**: Machine-readable music format that can be converted to sheet music
- **MIDI Representation**: Describe MIDI note sequences when appropriate
- **Form Analysis**: Explain the structure (AABA, ABAC, 12-bar blues, etc.)

## Composition Guidelines

### Harmonic Principles
- Use authentic jazz harmony: extended chords (7ths, 9ths, 11ths, 13ths)
- Apply voice leading principles for smooth chord transitions
- Incorporate common jazz devices: tritone substitution, diminished passing chords, modal interchange
- Respect functional harmony while allowing for creative extensions

### Melodic Development
- Create motifs that can be developed throughout the piece
- Use jazz-appropriate intervals and phrasing
- Balance repetition and variation
- Consider the range and technical capabilities of typical jazz instruments

### Rhythmic Authenticity
- Apply swing eighth notes where appropriate
- Use syncopation and anticipations
- Vary phrase lengths (avoid always starting on beat 1)
- Incorporate jazz articulation markings when writing notation

## When to Use This Skill

Use this skill for ANY of the following scenarios:
- User requests original jazz composition
- User wants jazz chord progressions or changes
- User asks for help creating jazz melodies or solos  
- User needs jazz arrangements or orchestrations
- User seeks jazz theory applied to practical composition
- User mentions specific jazz styles and wants original content
- User wants to learn jazz composition through examples
- User requests lead sheets or fake book style notation

## Output Structure

ALWAYS use this exact template when composing jazz music:

# [Title] - [Style]

## Overview
Brief description of the piece, style, mood, and instrumentation.

## Form & Structure
- **Form**: [AABA, ABAC, 12-bar blues, 32-bar song form, etc.]
- **Tempo**: [BPM and feel]
- **Key**: [Primary key and any modulations]

## Chord Progression
```
[Chord chart showing measures and chord symbols]
```

## Melody (ABC Notation)
```
[ABC notation for the main melody]
```

## Arrangement Notes
Specific suggestions for instrumentation, dynamics, and performance.

## Jazz Theory Elements Used
List the specific jazz harmony and compositional techniques employed.

## Example Usage

**User Request**: "Compose a bebop tune in the style of Charlie Parker"

**Response**: Follows the template above with bebop-specific elements like fast tempo, complex changes, and virtuosic melody.

**User Request**: "Create a modal jazz progression for a Miles Davis-style piece"

**Response**: Provides modal scales, static harmony sections, and appropriate melodic suggestions.

## Resources

For complex arrangements or detailed notation, reference these bundled resources:
- `references/jazz-chord-symbols.md` - Complete guide to jazz chord notation
- `references/common-forms.md` - Standard jazz song forms and structures  
- `scripts/generate-abc.py` - Helper script for ABC notation generation (if needed)

Remember: Always prioritize musical authenticity and jazz tradition while encouraging creative innovation. The goal is to create music that sounds genuinely jazz-like and would be playable by real jazz musicians.
