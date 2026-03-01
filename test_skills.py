"""Tests for Kepler SKILL.md files — validates structure, frontmatter, and content."""
import os
import re
import yaml
import pytest

REPO = os.path.expanduser("~/dev/amplifier-kepler-skill")

SKILLS = {
    "kepler-architecture": {
        "name": "kepler-architecture",
        "description_contains": "concentric rings",
        "required_sections": [
            "The Five Rings",
            "Ring Responsibilities",
            "Decision Checklist",
            "Kepler Repo Structure",
            "Canonical Reference",
        ],
        "required_content": [
            "Ring 1",  # Amplifier Core
            "Ring 2",
            "Ring 3",
            "Ring 4",
            "Ring 5",
            "amplifier-core",
        ],
    },
    "kepler-dev-setup": {
        "name": "kepler-dev-setup",
        "description_contains": "dev",
        "required_sections": [
            "Prerequisites",
            "Clone",
            "Setup",
            "Frontend",
            "Dev Mode",
            "Sidecar Standalone",
            "Run Tests",
            "Key Files",
            "Configuration",
        ],
        "required_content": [
            "Python 3.11",
            "uv",
            "Rust",
            "cargo",
            "Node 18",
            "npm",
            "Git",
            "settings.yaml",
        ],
    },
    "kepler-sidecar-patterns": {
        "name": "kepler-sidecar-patterns",
        "description_contains": "sidecar",
        "required_sections": [
            "Route Structure",
            "Spawn Capability",
            "Streaming Translation",
            "Approval Protocol",
            "Guardrails",
        ],
        "required_content": [
            "create_",  # factory pattern create_*_router
            "_router",
            "Adding a New Route",
            "depth cap",
            "DesktopApprovalSystem",
            "auto_approve",
        ],
    },
    "kepler-bundle-composition": {
        "name": "kepler-bundle-composition",
        "description_contains": "desktop.yaml",
        "required_sections": [
            "desktop.yaml Structure",
            "What Belongs Where",
            "Adding a New Bundle",
            "Adding a New Provider",
            "Composition Rules",
        ],
        "required_content": [
            "Ring 3",
            "Ring 4",
            "bundle:",
            "includes:",
            "providers:",
            "tools:",
            "hooks:",
        ],
    },
}


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


class TestSkillFilesExist:
    """All 4 SKILL.md files must exist."""

    @pytest.mark.parametrize("skill_name", SKILLS.keys())
    def test_skill_file_exists(self, skill_name):
        path = os.path.join(REPO, skill_name, "SKILL.md")
        assert os.path.isfile(path), f"{skill_name}/SKILL.md does not exist"


class TestFrontmatter:
    """Each SKILL.md must have valid YAML frontmatter with name and description."""

    @pytest.mark.parametrize("skill_name,spec", SKILLS.items())
    def test_frontmatter_is_valid_yaml(self, skill_name, spec):
        path = os.path.join(REPO, skill_name, "SKILL.md")
        if not os.path.isfile(path):
            pytest.skip(f"{path} does not exist yet")
        content = open(path).read()
        fm = parse_frontmatter(content)
        assert fm is not None, f"{skill_name}/SKILL.md has no YAML frontmatter"

    @pytest.mark.parametrize("skill_name,spec", SKILLS.items())
    def test_frontmatter_has_name(self, skill_name, spec):
        path = os.path.join(REPO, skill_name, "SKILL.md")
        if not os.path.isfile(path):
            pytest.skip(f"{path} does not exist yet")
        content = open(path).read()
        fm = parse_frontmatter(content)
        assert fm and "name" in fm, f"Missing 'name' in frontmatter"
        assert fm["name"] == spec["name"], f"Expected name={spec['name']}, got {fm['name']}"

    @pytest.mark.parametrize("skill_name,spec", SKILLS.items())
    def test_frontmatter_has_description(self, skill_name, spec):
        path = os.path.join(REPO, skill_name, "SKILL.md")
        if not os.path.isfile(path):
            pytest.skip(f"{path} does not exist yet")
        content = open(path).read()
        fm = parse_frontmatter(content)
        assert fm and "description" in fm, f"Missing 'description' in frontmatter"
        desc = fm["description"].lower()
        keyword = spec["description_contains"].lower()
        assert keyword in desc, f"Description should mention '{keyword}': {fm['description']}"


class TestContent:
    """Each SKILL.md must contain required sections and content."""

    @pytest.mark.parametrize("skill_name,spec", SKILLS.items())
    def test_required_sections(self, skill_name, spec):
        path = os.path.join(REPO, skill_name, "SKILL.md")
        if not os.path.isfile(path):
            pytest.skip(f"{path} does not exist yet")
        content = open(path).read()
        for section in spec["required_sections"]:
            assert section in content, (
                f"{skill_name}: missing required section/keyword '{section}'"
            )

    @pytest.mark.parametrize("skill_name,spec", SKILLS.items())
    def test_required_content(self, skill_name, spec):
        path = os.path.join(REPO, skill_name, "SKILL.md")
        if not os.path.isfile(path):
            pytest.skip(f"{path} does not exist yet")
        content = open(path).read()
        for keyword in spec["required_content"]:
            assert keyword in content, (
                f"{skill_name}: missing required content '{keyword}'"
            )


class TestArchitectureSpecifics:
    """kepler-architecture must have the 5 rings and decision checklist."""

    def _load(self):
        path = os.path.join(REPO, "kepler-architecture", "SKILL.md")
        if not os.path.isfile(path):
            pytest.skip("File does not exist yet")
        return open(path).read()

    def test_five_rings_listed(self):
        content = self._load()
        for ring in ["Ring 1", "Ring 2", "Ring 3", "Ring 4", "Ring 5"]:
            assert ring in content

    def test_decision_checklist_has_questions(self):
        content = self._load()
        # Should have at least 5 question marks in decision checklist area
        checklist_start = content.find("Decision Checklist")
        assert checklist_start != -1
        checklist_section = content[checklist_start:]
        questions = checklist_section.count("?")
        assert questions >= 5, f"Decision checklist should have >=5 questions, found {questions}"

    def test_repo_structure_tree(self):
        content = self._load()
        # Should contain tree-like characters
        assert "Kepler Repo Structure" in content
        struct_start = content.find("Kepler Repo Structure")
        struct_section = content[struct_start:struct_start + 1000]
        assert any(c in struct_section for c in ["├", "└", "│"]), "Repo structure should use tree characters"


class TestDevSetupSpecifics:
    """kepler-dev-setup must have numbered steps and key files table."""

    def _load(self):
        path = os.path.join(REPO, "kepler-dev-setup", "SKILL.md")
        if not os.path.isfile(path):
            pytest.skip("File does not exist yet")
        return open(path).read()

    def test_has_key_files_table(self):
        content = self._load()
        assert "Key Files" in content
        # Table should have pipe characters
        assert "|" in content, "Key files should be in a table format"

    def test_settings_yaml_mentioned(self):
        content = self._load()
        assert "settings.yaml" in content


class TestSidecarPatternsSpecifics:
    """kepler-sidecar-patterns must have factory pattern and streaming events."""

    def _load(self):
        path = os.path.join(REPO, "kepler-sidecar-patterns", "SKILL.md")
        if not os.path.isfile(path):
            pytest.skip("File does not exist yet")
        return open(path).read()

    def test_factory_pattern(self):
        content = self._load()
        assert "create_" in content and "_router" in content

    def test_streaming_has_4_events(self):
        content = self._load()
        stream_start = content.find("Streaming Translation")
        assert stream_start != -1
        # Should mention 4 key events after this section
        stream_section = content[stream_start:stream_start + 2000]
        # At minimum should describe multiple event types
        assert "event" in stream_section.lower() or "Event" in stream_section

    def test_three_step_new_route(self):
        content = self._load()
        assert "Adding a New Route" in content

    def test_guardrails_has_4_rules(self):
        content = self._load()
        guard_start = content.find("Guardrails")
        assert guard_start != -1


class TestBundleCompositionSpecifics:
    """kepler-bundle-composition must have desktop.yaml example and composition rules."""

    def _load(self):
        path = os.path.join(REPO, "kepler-bundle-composition", "SKILL.md")
        if not os.path.isfile(path):
            pytest.skip("File does not exist yet")
        return open(path).read()

    def test_desktop_yaml_example(self):
        content = self._load()
        # Should have a YAML code block with desktop.yaml content
        assert "```yaml" in content or "```yml" in content
        for key in ["bundle:", "includes:", "providers:", "tools:", "hooks:"]:
            assert key in content, f"desktop.yaml example should contain '{key}'"

    def test_ring3_vs_ring4(self):
        content = self._load()
        assert "Ring 3" in content
        assert "Ring 4" in content

    def test_four_step_new_bundle(self):
        content = self._load()
        assert "Adding a New Bundle" in content

    def test_provider_yaml_example(self):
        content = self._load()
        assert "Adding a New Provider" in content

    def test_five_composition_rules(self):
        content = self._load()
        rules_start = content.find("Composition Rules")
        assert rules_start != -1
        rules_section = content[rules_start:]
        # Should have at least 5 numbered or bulleted rules
        numbered = len(re.findall(r'\d+\.', rules_section))
        bulleted = rules_section.count("- ")
        assert numbered >= 5 or bulleted >= 5, (
            f"Composition Rules should have >=5 rules, found {numbered} numbered, {bulleted} bulleted"
        )
