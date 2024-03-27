(() => {
	const palettes = window.CHIROPTERA_PALETTES;
	const paletteLab = window.CHIROPTERA_PALETTE_LAB;
	const paletteGroups = [
		{ label: "Workspace surfaces", names: ["bg.dim", "bg", "bg.bright"], half: true },
		{ label: "Text roles", names: ["fg.dim", "fg", "fg.bright"], half: true },
		{ label: "Context & state", names: ["red.dim", "yellow.dim", "green.dim", "cyan.dim", "blue.dim", "magenta.dim"] },
		{ label: "Everyday UI", names: ["red", "yellow", "green", "cyan", "blue", "magenta"] },
		{ label: "Syntax & emphasis", names: ["red.bright", "yellow.bright", "green.bright", "cyan.bright", "blue.bright", "magenta.bright"] },
	];
	const paletteSwatches = new Map();
	const grid = document.querySelector("#palette-grid");
	const templateSample = document.querySelector("#template-sample");
	const generatedTemplate = document.querySelector("#generated-template");
	const inspectCommand = document.querySelector("#inspect-command");
	const renderCommand = document.querySelector("#render-command");
	const paletteWing = document.querySelector("#palette-wing");
	const editorScreenshot = document.querySelector("#editor-screenshot");
	const editorScreenshotCaption = document.querySelector("#editor-screenshot-caption");
	const labChart = document.querySelector("#lab-chart");
	const labTooltip = document.querySelector("#lab-tooltip");
	const contrastNote = document.querySelector("#contrast-note");
	const parameters = new URLSearchParams(window.location.search);
	const requestedContrast = parameters.get("contrast");
	let mode = document.documentElement.dataset.themeMode || "auto";
	let contrast = ["hard", "normal", "soft"].includes(requestedContrast) ? requestedContrast : "normal";

	function resolvedMode() {
		return window.SiteUi.theme.resolveTheme(mode);
	}

	function readableInk(hex) {
		const [red, green, blue] = [1, 3, 5].map((start) => Number.parseInt(hex.slice(start, start + 2), 16));
		return (red * 299 + green * 587 + blue * 114) / 1000 > 150 ? "#242425" : "#f6f1da";
	}

	function label(name) { return name.replace(".", " · "); }

	function createSwatch(name) {
		const button = document.createElement("button");
		button.className = "ui-swatch";
		button.type = "button";
		button.innerHTML = `<span class="ui-swatch-color"></span><span class="ui-swatch-label"></span><span class="ui-swatch-name">${label(name)}</span>`;
		button.addEventListener("click", () => copy(button.dataset.hex, button));
		paletteSwatches.set(name, button);
		return button;
	}

	function updateSwatch(name, palette) {
		const button = paletteSwatches.get(name);
		const hex = palette[name];
		button.dataset.hex = hex;
		button.style.setProperty("--ui-swatch-bg", hex);
		button.style.setProperty("--ui-swatch-ink", readableInk(hex));
		button.querySelector(".ui-swatch-label").textContent = hex;
	}

	function positionLabTooltip(event) {
		const bounds = labTooltip.parentElement.getBoundingClientRect();
		labTooltip.style.left = `${event.clientX - bounds.left + 12}px`;
		labTooltip.style.top = `${event.clientY - bounds.top - 34}px`;
	}

	function renderLabChart(paletteMode, contrast, palette) {
		const lab = paletteLab[paletteMode][contrast];
		const lanes = [
			["background", "bg.dim", "bg", "bg.bright"],
			["foreground", "fg.dim", "fg", "fg.bright"],
			["red", "red.dim", "red", "red.bright"],
			["yellow", "yellow.dim", "yellow", "yellow.bright"],
			["green", "green.dim", "green", "green.bright"],
			["cyan", "cyan.dim", "cyan", "cyan.bright"],
			["blue", "blue.dim", "blue", "blue.bright"],
			["magenta", "magenta.dim", "magenta", "magenta.bright"],
		];
		const left = 104;
		const right = 34;
		const top = 45;
		const laneHeight = 40;
		const width = 760 - left - right;
		const x = (lightness) => left + width * lightness / 100;
		const roleGroups = [
			{ label: "workspace surfaces", members: ["bg.dim", "bg", "bg.bright"], start: 0, end: 0, labelOffset: -6 },
			{ label: "context & state", members: ["red.dim", "yellow.dim", "green.dim", "cyan.dim", "blue.dim", "magenta.dim"], start: 2, end: 7, labelOffset: -6 },
			{ label: "supporting text", members: ["fg.dim"], start: 1, end: 1, labelOffset: 44 },
			{ label: "everyday text & UI", members: ["fg", "red", "yellow", "green", "cyan", "blue", "magenta"], start: 1, end: 7, labelOffset: -6, labelAlign: paletteMode === "dark" ? "end" : "start" },
			{ label: "syntax & emphasis", members: ["fg.bright", "red.bright", "yellow.bright", "green.bright", "cyan.bright", "blue.bright", "magenta.bright"], start: 1, end: 7, labelOffset: -6, labelAlign: paletteMode === "dark" ? "start" : "end" },
		];
		const roleBounds = (group) => {
			const positions = group.members.map((name) => x(lab[name].l));
			const min = Math.min(...positions) - 18;
			const max = Math.max(...positions) + 18;
			const y = top + group.start * laneHeight - 17;
			const labelAlign = group.labelAlign || "middle";
			const labelX = labelAlign === "start" ? min : labelAlign === "end" ? max : min + (max - min) / 2;
			return { x: min, y, width: max - min, height: (group.end - group.start) * laneHeight + 34, labelX, labelY: y + group.labelOffset, labelAlign };
		};
		const animatePosition = (element, positions) => {
			if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
				Object.entries(positions).forEach(([property, value]) => element.setAttribute(property, value));
				return;
			}

			if (element.labAnimationFrame != null) cancelAnimationFrame(element.labAnimationFrame);
			const start = Object.fromEntries(Object.entries(positions).map(([property]) => (
				[property, Number.parseFloat(element.getAttribute(property))]
			)));
			const startedAt = performance.now();
			const duration = 420;
			const step = (now) => {
				const progress = Math.min((now - startedAt) / duration, 1);
				const eased = 1 - (1 - progress) ** 3;
				Object.entries(positions).forEach(([property, value]) => {
					element.setAttribute(property, start[property] + (value - start[property]) * eased);
				});
				if (progress < 1) element.labAnimationFrame = requestAnimationFrame(step);
				else delete element.labAnimationFrame;
			};
			element.labAnimationFrame = requestAnimationFrame(step);
		};

		if (labChart.dataset.rendered === "true") {
			labChart.querySelectorAll(".lab-role-group").forEach((element) => {
				const group = roleGroups[Number.parseInt(element.dataset.group, 10)];
				const bounds = roleBounds(group);
				const box = element.querySelector("rect");
				animatePosition(box, { x: bounds.x, width: bounds.width });
				box.setAttribute("y", bounds.y);
				box.setAttribute("height", bounds.height);
				const label = element.querySelector("text");
				animatePosition(label, { x: bounds.labelX });
				label.setAttribute("y", bounds.labelY);
				label.setAttribute("text-anchor", bounds.labelAlign);
			});
			labChart.querySelectorAll(".lab-dot").forEach((dot) => {
				const color = dot.dataset.color;
				const lightness = lab[color].l;
				animatePosition(dot, { cx: x(lightness) });
				dot.setAttribute("fill", palette[color]);
				dot.dataset.lightness = lightness;
			});
			labChart.querySelectorAll(".lab-connection").forEach((connection) => {
				animatePosition(connection, {
					x1: x(lab[connection.dataset.from].l),
					x2: x(lab[connection.dataset.to].l),
				});
			});
			return;
		}

		const guides = [0, 25, 50, 75, 100].map((lightness) => (
			`<line class="lab-guide" x1="${x(lightness)}" x2="${x(lightness)}" y1="${top - 18}" y2="${top + laneHeight * lanes.length - 18}"/><text class="lab-tick" x="${x(lightness)}" y="19">${lightness}</text>`
		)).join("");
		const rows = lanes.map(([name, ...colors], index) => {
			const y = top + index * laneHeight;
			const dots = colors.map((color) => (
				`<circle class="lab-dot" cx="${x(lab[color].l)}" cy="${y}" r="7" fill="${palette[color]}" data-color="${color}" data-label="${label(color)}" data-lightness="${lab[color].l}"/>`
			)).join("");
			const connections = colors.slice(1).map((color, colorIndex) => (
				`<line class="lab-connection" x1="${x(lab[colors[colorIndex]].l)}" x2="${x(lab[color].l)}" y1="${y}" y2="${y}" data-from="${colors[colorIndex]}" data-to="${color}"/>`
			)).join("");
			return `<text class="lab-label" x="${left - 17}" y="${y + 4}">${name}</text><line class="lab-lane" x1="${left}" x2="${left + width}" y1="${y}" y2="${y}"/>${connections}${dots}`;
		}).join("");
		const groupOutlines = roleGroups.map((group, index) => {
			const bounds = roleBounds(group);
			return `<g class="lab-role-group" data-group="${index}"><rect x="${bounds.x}" y="${bounds.y}" width="${bounds.width}" height="${bounds.height}" rx="11"/><text x="${bounds.labelX}" y="${bounds.labelY}" text-anchor="${bounds.labelAlign}">${group.label}</text></g>`;
		}).join("");
		labChart.innerHTML = `<text class="lab-axis" x="${left - 17}" y="19">LAB · L*</text>${guides}${groupOutlines}${rows}`;
		labChart.dataset.rendered = "true";
		labChart.querySelectorAll(".lab-dot").forEach((dot) => {
			dot.addEventListener("pointerenter", (event) => {
				labTooltip.textContent = `${dot.dataset.label} · L* ${dot.dataset.lightness}`;
				labTooltip.hidden = false;
				positionLabTooltip(event);
			});
			dot.addEventListener("pointermove", positionLabTooltip);
			dot.addEventListener("pointerleave", () => { labTooltip.hidden = true; });
		});
	}

	function selectWingSegment(event) {
		const bounds = paletteWing.getBoundingClientRect();
		const horizontal = event.clientX - bounds.left - bounds.width / 2;
		const vertical = event.clientY - bounds.top - bounds.height / 2;
		const radius = Math.hypot(horizontal, vertical);
		if (radius < Math.min(bounds.width, bounds.height) * .16) return;
		const paletteMode = resolvedMode();
		const rotation = 180 + (paletteMode === "light" ? 180 : 0)
			+ ({ hard: 60, normal: 0, soft: -60 })[contrast];
		const angle = Math.atan2(vertical, horizontal) * 180 / Math.PI - rotation;
		const segment = [
			{ mode: "dark", contrast: "normal" },
			{ mode: "dark", contrast: "soft" },
			{ mode: "light", contrast: "hard" },
			{ mode: "light", contrast: "normal" },
			{ mode: "light", contrast: "soft" },
			{ mode: "dark", contrast: "hard" },
		][((Math.round(angle / 60) % 6) + 6) % 6];
		contrast = segment.contrast;
		window.SiteUi.theme.applyTheme(segment.mode);
		window.SiteUi.url.setOwnedParameter("contrast", contrast, "normal");
		render();
	}

	async function copy(hex, button) {
		try { await window.SiteUi.copy.withFeedback(button.querySelector(".ui-swatch-color"), hex); } catch (_) { return; }
	}

	function render() {
		window.SiteUi.url.setOwnedParameters([
			{ name: "theme", value: mode, defaultValue: "auto" },
			{ name: "contrast", value: contrast, defaultValue: "normal" },
		]);
		const paletteMode = resolvedMode();
		const palette = palettes[paletteMode][contrast];
		const vimSample = window.CHIROPTERA_VIM_SAMPLES[paletteMode][contrast];
		const scheme = `chiroptera_${paletteMode}_${contrast}`;
		document.documentElement.dataset.paletteMode = paletteMode;
		document.documentElement.dataset.paletteContrast = contrast;
		document.documentElement.style.setProperty("--bg", palette.bg);
		document.documentElement.style.setProperty("--panel", palette["bg.bright"]);
		document.documentElement.style.setProperty("--ink", palette["fg.bright"]);
		document.documentElement.style.setProperty("--copy", palette.fg);
		document.documentElement.style.setProperty("--muted", palette["fg.dim"]);
		document.documentElement.style.setProperty("--accent", palette["cyan.bright"]);
		document.documentElement.style.setProperty("--accent-warm", palette["yellow.bright"]);
		document.documentElement.style.setProperty("color-scheme", paletteMode);
		renderLabChart(paletteMode, contrast, palette);
		templateSample.innerHTML = vimSample.template;
		generatedTemplate.innerHTML = vimSample.generated;
		inspectCommand.innerHTML = vimSample.inspect;
		renderCommand.innerHTML = vimSample.render;
		document.querySelector("#generated-template-title").textContent = `Generated Vim · ${paletteMode} ${contrast}`;
		editorScreenshot.src = `assets/screenshots/${scheme}.png`;
		editorScreenshot.alt = `Neovim editing a Python file with the chiroptera ${paletteMode} ${contrast} colorscheme.`;
		editorScreenshotCaption.textContent = `Neovim · ${paletteMode} ${contrast} · Python`;
		contrastNote.textContent = {
			hard: "Hard · WCAG AA for normal text, with the highest contrast.",
			normal: "Normal · WCAG AA for normal text, balanced for daily use.",
			soft: "Soft · Lower contrast by design; use bright text if WCAG AA is needed.",
		}[contrast];
		if (!grid.hasChildNodes()) {
			grid.replaceChildren(...paletteGroups.map((group) => {
				const section = document.createElement("section");
				section.className = `palette-group${group.half ? " palette-group--half" : ""}`;
				section.setAttribute("aria-label", group.label);
				const heading = document.createElement("h3");
				heading.className = "palette-group-label";
				heading.textContent = group.label;
				const swatches = document.createElement("div");
				swatches.className = "palette-group-swatches";
				swatches.replaceChildren(...group.names.map(createSwatch));
				section.replaceChildren(heading, swatches);
				return section;
			}));
		}
		paletteGroups.forEach((group) => group.names.forEach((name) => updateSwatch(name, palette)));
		document.querySelectorAll(".ui-theme-option[data-theme-mode]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.themeMode === mode)));
		document.querySelectorAll("[data-contrast]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.contrast === contrast)));
	}

	document.querySelectorAll("[data-contrast]").forEach((button) => button.addEventListener("click", () => {
		contrast = button.dataset.contrast;
		window.SiteUi.url.setOwnedParameter("contrast", contrast, "normal");
		render();
	}));
	paletteWing.addEventListener("click", selectWingSegment);
	window.addEventListener("siteui:themechange", (event) => {
		mode = event.detail.mode;
		render();
	});
	render();
})();
