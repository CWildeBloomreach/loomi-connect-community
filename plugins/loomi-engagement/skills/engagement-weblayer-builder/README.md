# Bloomreach weblayer builder

Builds, edits and fixes the HTML, CSS and JavaScript for Bloomreach Engagement weblayers: pop-ups, slide-ins, inline embeds, exit-intent overlays, email and phone capture, countdowns and recommendation widgets. The code follows the platform skeleton, makes every colour, size and piece of copy a template parameter, and is checked against the rules that stop weblayers rendering. With Loomi Connect connected, it reads an existing weblayer's code before changing it. Dynamic data (recommendations, cart items, catalogs, reports) is written with [engagement-jinja-writer](../engagement-jinja-writer/), so the Jinja rules live in one place.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | Optional: `list_cloud_organizations`, `list_projects`, `search_banners` |
| **Other requirements** | None. Works without Loomi Connect if the user pastes the existing code. Uses the engagement-jinja-writer skill for dynamic data |
| **Tested with** | Claude Code: the weblayer skeleton and rules have been used day to day to build live weblayers. Project resolution and `search_banners` (list, archived list and one weblayer by ID) were run read-only against a test project on 2026-10-30, and the variant fields, the source versus rendered code and the archived-list step come from that run. Not tested: building a weblayer end to end through the skill, rendering (Loomi Connect can't preview a weblayer), triggering in a fresh session, and any OpenAI client. |
| **Maintainer** | @CWildeBloomreach |

## Example prompts

- "Build a newsletter sign-up pop-up in our brand colours, with a 10% off success message."
- "Turn this design into a Bloomreach weblayer." (with a screenshot or Figma export)
- "Add a 'You might also like' row with four recommendations to our exit-intent weblayer."
- "Our weblayer is active but doesn't show. Can you fix it?"
- "Make the copy and colours of the 'Spring sale' weblayer editable as parameters."

## Example output

See [examples/fix-weblayer-not-showing.md](examples/fix-weblayer-not-showing.md).

## Notes and limitations

- The skill only returns code. Loomi Connect has no tool that creates or changes a weblayer, so the user pastes it into Bloomreach.
- Loomi Connect calls weblayers **banners**. Each variant's source code (with parameters) and its rendered copy (with current values) are both returned; the skill edits the source.
- Preview the weblayer in Bloomreach and on the site before it goes live. The skill can't render it.
- The platform reference was checked against the Bloomreach documentation on 2026-10-30. The `utils` helper library, `self.inPreview` and the phone-input setup come from Bloomreach's built-in weblayer templates and aren't publicly documented.
- Identifying a customer depends on the project's hard ID: a plain string sets `registered`, so the skill asks which ID the project uses.
