"""Tests for Kepler SKILL.md files — validates structure, frontmatter, and content."""

import os
import re

import pytest
import yaml

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


def _read_skill(skill_name: str) -> str:
    """Read a SKILL.md file, skipping the test if it doesn't exist yet."""
    path = os.path.join(REPO, skill_name, "SKILL.md")
    if not os.path.isfile(path):
        pytest.skip(f"{path} does not exist yet")
    with open(path) as f:
        return f.read()


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
        content = _read_skill(skill_name)
        fm = parse_frontmatter(content)
        assert fm is not None, f"{skill_name}/SKILL.md has no YAML frontmatter"

    @pytest.mark.parametrize("skill_name,spec", SKILLS.items())
    def test_frontmatter_has_name(self, skill_name, spec):
        content = _read_skill(skill_name)
        fm = parse_frontmatter(content)
        assert fm and "name" in fm, "Missing 'name' in frontmatter"
        assert fm["name"] == spec["name"], (
            f"Expected name={spec['name']}, got {fm['name']}"
        )

    @pytest.mark.parametrize("skill_name,spec", SKILLS.items())
    def test_frontmatter_has_description(self, skill_name, spec):
        content = _read_skill(skill_name)
        fm = parse_frontmatter(content)
        assert fm and "description" in fm, "Missing 'description' in frontmatter"
        desc = fm["description"].lower()
        keyword = spec["description_contains"].lower()
        assert keyword in desc, (
            f"Description should mention '{keyword}': {fm['description']}"
        )


class TestContent:
    """Each SKILL.md must contain required sections and content."""

    @pytest.mark.parametrize("skill_name,spec", SKILLS.items())
    def test_required_sections(self, skill_name, spec):
        content = _read_skill(skill_name)
        for section in spec["required_sections"]:
            assert section in content, (
                f"{skill_name}: missing required section/keyword '{section}'"
            )

    @pytest.mark.parametrize("skill_name,spec", SKILLS.items())
    def test_required_content(self, skill_name, spec):
        content = _read_skill(skill_name)
        for keyword in spec["required_content"]:
            assert keyword in content, (
                f"{skill_name}: missing required content '{keyword}'"
            )


class TestArchitectureSpecifics:
    """kepler-architecture must have the 5 rings and decision checklist."""

    def test_five_rings_listed(self):
        content = _read_skill("kepler-architecture")
        for ring in ["Ring 1", "Ring 2", "Ring 3", "Ring 4", "Ring 5"]:
            assert ring in content

    def test_decision_checklist_has_questions(self):
        content = _read_skill("kepler-architecture")
        # Should have at least 5 question marks in decision checklist area
        checklist_start = content.find("Decision Checklist")
        assert checklist_start != -1
        checklist_section = content[checklist_start : checklist_start + 2000]
        questions = checklist_section.count("?")
        assert questions >= 5, (
            f"Decision checklist should have >=5 questions, found {questions}"
        )

    def test_repo_structure_tree(self):
        content = _read_skill("kepler-architecture")
        # Should contain tree-like characters
        assert "Kepler Repo Structure" in content
        struct_start = content.find("Kepler Repo Structure")
        struct_section = content[struct_start : struct_start + 1000]
        assert any(c in struct_section for c in ["├", "└", "│"]), (
            "Repo structure should use tree characters"
        )


class TestDevSetupSpecifics:
    """kepler-dev-setup must have numbered steps and key files table."""

    def test_has_key_files_table(self):
        content = _read_skill("kepler-dev-setup")
        key_files_start = content.find("Key Files")
        assert key_files_start != -1, "Missing 'Key Files' section"
        key_files_section = content[key_files_start : key_files_start + 2000]
        # Table should have pipe characters within the Key Files section
        assert "|" in key_files_section, "Key files should be in a table format"

    def test_settings_yaml_mentioned(self):
        content = _read_skill("kepler-dev-setup")
        assert "settings.yaml" in content


class TestSidecarPatternsSpecifics:
    """kepler-sidecar-patterns must have factory pattern and streaming events."""

    def test_factory_pattern(self):
        content = _read_skill("kepler-sidecar-patterns")
        assert "create_" in content and "_router" in content

    def test_streaming_has_4_events(self):
        content = _read_skill("kepler-sidecar-patterns")
        stream_start = content.find("Streaming Translation")
        assert stream_start != -1
        stream_section = content[stream_start : stream_start + 2000]
        # Verify all 4 specific event names are present
        for event in ["token", "tool_call", "tool_result", "turn_complete"]:
            assert event in stream_section, (
                f"Streaming section should describe '{event}' event"
            )

    def test_three_step_new_route(self):
        content = _read_skill("kepler-sidecar-patterns")
        route_start = content.find("Adding a New Route")
        assert route_start != -1
        route_section = content[route_start : route_start + 1000]
        # Verify all 3 numbered steps are present
        for step in ["1.", "2.", "3."]:
            assert step in route_section, f"Adding a New Route should have step {step}"

    def test_guardrails_has_4_rules(self):
        content = _read_skill("kepler-sidecar-patterns")
        guard_start = content.find("Guardrails")
        assert guard_start != -1
        guard_section = content[guard_start:]
        # Verify all 4 numbered rules are present
        for rule_num in ["1.", "2.", "3.", "4."]:
            assert rule_num in guard_section, f"Guardrails should have rule {rule_num}"


class TestBundleCompositionSpecifics:
    """kepler-bundle-composition must have desktop.yaml example and composition rules."""

    def test_desktop_yaml_example(self):
        content = _read_skill("kepler-bundle-composition")
        # Should have a YAML code block with desktop.yaml content
        assert "```yaml" in content or "```yml" in content
        for key in ["bundle:", "includes:", "providers:", "tools:", "hooks:"]:
            assert key in content, f"desktop.yaml example should contain '{key}'"

    def test_ring3_vs_ring4(self):
        content = _read_skill("kepler-bundle-composition")
        assert "Ring 3" in content
        assert "Ring 4" in content

    def test_four_step_new_bundle(self):
        content = _read_skill("kepler-bundle-composition")
        bundle_start = content.find("Adding a New Bundle")
        assert bundle_start != -1
        bundle_section = content[bundle_start : bundle_start + 1500]
        # Verify all 4 numbered steps are present
        for step in ["1.", "2.", "3.", "4."]:
            assert step in bundle_section, (
                f"Adding a New Bundle should have step {step}"
            )

    def test_provider_yaml_example(self):
        content = _read_skill("kepler-bundle-composition")
        provider_start = content.find("Adding a New Provider")
        assert provider_start != -1
        provider_section = content[provider_start : provider_start + 1000]
        # Verify provider YAML example has key structure
        for key in ["providers:", "models:", "default:"]:
            assert key in provider_section, (
                f"Adding a New Provider section should contain '{key}'"
            )

    def test_five_composition_rules(self):
        content = _read_skill("kepler-bundle-composition")
        rules_start = content.find("Composition Rules")
        assert rules_start != -1
        rules_section = content[rules_start:]
        # Should have at least 5 numbered or bulleted rules
        numbered = len(re.findall(r"^\d+\.", rules_section, re.MULTILINE))
        bulleted = rules_section.count("- ")
        assert numbered >= 5 or bulleted >= 5, (
            f"Composition Rules should have >=5 rules, found {numbered} numbered, {bulleted} bulleted"
        )
