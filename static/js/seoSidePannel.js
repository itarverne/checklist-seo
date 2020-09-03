document.addEventListener('DOMContentLoaded', function () {

	var e = React.createElement;
	sidePannel = document.createElement('div');
	sidePannel.classList.add("seo_side_pannel")
	document.getElementById('tab-settings').after(sidePannel);
	class SeoSideBar extends React.Component {
		constructor(props) {
			super(props);
			this.state = {
				keywordScore: 0,
				lengthScore: 0,
				titleScore: 0,
				urlScore: 0,
				internalLinksScore: 0,
				seoBodyInputTimeout: null,
				seoKeyWordInputTimeout: null,
				seoTitleInputTimeout: null,
				seoSlugInputTimeout: null,
				seoTimeRefresh: document.getElementById("id_delay_keyword").value * 1000,
				keywordValidationColor: "gray",
				keywordValidationPercentage: "NK",
				keywordIndicatorTitle: "There is no keyword, please add a keyword via the seo pannel",
				titleValidationColor: "red",
				lengthValidationColor: "red",
				slugValidationColor: "red",
				internalLinksValidationColor: "red",
				internalLinks: 0,
				length: 0,
				titleWords: 0,
				titleCharacters: 0,
				h1_in_content_warning: ""
			};
			document.getElementById("id_delay_keyword").addEventListener('change', () => {
				let seoTimeRefresh = document.getElementById("id_delay_keyword").value;
				if (seoTimeRefresh < 0) document.getElementById("id_delay_keyword").value = 0;
				if (seoTimeRefresh > 99) document.getElementById("id_delay_keyword").value = 99;
				this.setState({ seoTimeRefresh: document.getElementById("id_delay_keyword").value * 1000 });
			});
			document.getElementById("id_keyword").addEventListener('keyup', () => {
				clearTimeout(this.state.seoKeyWordInputTimeout);
				this.setState({
					seoKeyWordInputTimeout: setTimeout(() => {
						this.checkKeyword();
						this.checkValidation();
					}, this.state.seoTimeRefresh)
				});
			});
			document.getElementById("body-list").addEventListener('keyup', () => {
				clearTimeout(this.state.seoBodyInputTimeout);
				this.setState({
					seoBodyInputTimeout: setTimeout(() => {
						this.checkKeyword();
						this.checkLength();
						this.checkInternalLinks();
						this.check_h1_in_content();
						this.checkValidation();
					}, this.state.seoTimeRefresh)
				});
			});

			// removal of all h1 buttons in rich text fields
			for (let stream_field of document.getElementsByClassName("stream-field")) {
				stream_field.addEventListener('click', (e) => {
					if (document.querySelectorAll('button.Draftail-ToolbarButton[name="header-one"]').length != 0) {
						for (let h1_button of document.querySelectorAll('button[name="header-one"]')) {
							h1_button.style.display = "none";
						}
					}
				});
			}
			document.getElementById("id_title").addEventListener("input", () => {
				clearTimeout(this.state.seoTitleInputTimeout);
				this.setState({
					seoTitleInputTimeout: setTimeout(() => {
						this.checkTitle();
						this.checkValidation();
					}, this.state.seoTimeRefresh)
				});
			});
			document.getElementById("id_slug").addEventListener("input", () => {
				clearTimeout(this.state.seoSlugInputTimeout);
				this.setState({
					seoSlugInputTimeout: setTimeout(() => {
						this.checkSlug();
						this.checkValidation();
					}, this.state.seoTimeRefresh)
				});
			});
			this.checkValidation();
		}
		checkValidation() {
			var seoScore = this.state.keywordScore + this.state.lengthScore
				+ this.state.titleScore + this.state.urlScore
				+ this.state.internalLinksScore;
			if ((seoScore / 5) >= 0.8) {
				this.enablePublish();
			} else {
				this.disablePublish();
			}
		}
		getText() {
			let blocks = document.getElementsByClassName("notranslate public-DraftEditor-content");
			let text = "";
			for (let block of blocks) {
				// we make sure we don’t get deleted blocks’s content
				if (block.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode
					.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.style.display != "none") {
					// we make sure we get only text and not GistCreateCode code
					if (block.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode
						.parentNode.parentNode.parentNode.parentNode.children[0].children[2].children[0].innerHTML != "Code") {
						for (let line of block.firstChild.children) {
							if (!line.classList.contains('Draftail-block--atomic')) {
								if (line.classList.contains('public-DraftStyleDefault-ol')
									|| line.classList.contains('public-DraftStyleDefault-ul')) {
									for (let child of line.children) {
										text += " " + child.firstChild.firstChild.firstChild.innerHTML;
									}
								}
								else {
									for (let group of line.firstChild.children) {
										if (!group.classList.contains("TooltipEntity")) {
											text += " " + group.firstChild.innerHTML;
										}
										// if there are links in the article, we get only the text of the link
										else {
											text += " " + group.children[1].firstChild.innerHTML;
										}
									}
								}
							}
						}
					}
				}
			}
			return text;
		}
		getHtml() {
			var rich_text_blocks = document.getElementsByClassName("notranslate public-DraftEditor-content");
			var raw_html_blocks = document.querySelectorAll('textarea[placeholder="RawHtml"]');
			var text = "";
			for (let block of rich_text_blocks) {
				// we make sure we don’t get deleted blocks’s content
				if (block.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode
					.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.style.display != "none") {
					// we make sure we get only text and not GistCreateCode code
					if (block.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode
						.parentNode.parentNode.parentNode.children[0].children[2].children[0].innerHTML != "Code") {
						text += block.firstChild.firstChild.firstChild.innerHTML;
					}
				}
			}
			for (let block of raw_html_blocks) {
				if (block.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode
					.parentNode.parentNode.style.display != "none") {
					text += block.value;
				}
			}
			return text;
		}
		enablePublish() {
			let publishButtons = document.getElementsByName("action-publish");
			for (let button of publishButtons) {
				button.disabled = false;
				button.title = "";
			}
			let submitButtons = document.getElementsByName("action-submit");
			for (let button of submitButtons) {
				button.disabled = false;
				button.title = "";
			}
		}
		disablePublish() {
			let publishButtons = document.getElementsByName("action-publish");
			for (let button of publishButtons) {
				button.disabled = 'disabled';
				button.title = "Publishing is disabled as the SEO recommandations are not met, be sure "
					+ "to get at least 80% SEO validation to continue";
			}
			let submitButtons = document.getElementsByName("action-submit");
			for (let button of submitButtons) {
				button.disabled = 'disabled';
				button.title = "Publishing is disabled as the SEO recommandations are not met, be sure "
					+ "to get at least 80% SEO validation to continue";
			}
		}
		checkKeyword() {
			let body = [];
			body[0] = document.getElementById("id_keyword").value;
			body[1] = this.getText();
			fetch("/seo/keyword/", {
				method: "POST",
				credentials: 'include',
				body: JSON.stringify(body),
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
					'X-Requested-With': 'XMLHttpRequest',
					'Content-Type': 'application/json',
					'Accept': 'application/json'
				},
				dataType: "json"
			}).then((response) => {
				return response.json();
			}).then((data) => {
				if (data['response'] == "NO_KEYWORD") {
					this.setState({
						keywordScore: 0,
						keywordValidationPercentage: "NK",
						keywordValidationColor: "gray",
						keywordIndicatorTitle: "There is no keyword, please add a keyword via the seo pannel"
					});
				}
				else if (data['response'] == "INVALID_KEYWORD" || data['response'] == "NO_TEXT") {
					this.setState({
						keywordScore: 0,
						keywordValidationPercentage: (data['response'] == "NO_TEXT") ? "NT" : `${(Math.round(data['percentage'] * 10) / 10)} %`,
						keywordValidationColor: (data['response'] == "NO_TEXT") ? "gray" : "red",
						keywordIndicatorTitle: (data['response'] == "NO_TEXT") ? "There is no text, please add some text in the "
							+ "article" : "Your keyword is not validated because it is too frequent or too rare (2% or less or above 3%)"
					});
				}
				else if (data['response'] == "VALID_KEYWORD") {
					this.setState({
						keywordScore: 1,
						keywordValidationPercentage: `${(Math.round(data['percentage'] * 10) / 10).toString()} %`,
						keywordValidationColor: "green",
						keywordIndicatorTitle: "The keyword is present and the frequence matches the seo recommendations"
					});
				}
			});
		}
		checkLength() {
			fetch("/seo/length/", {
				method: "POST",
				credentials: 'include',
				body: JSON.stringify(this.getText()),
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
					'X-Requested-With': 'XMLHttpRequest',
					'Content-Type': 'application/json',
					'Accept': 'application/json'
				},
				dataType: "json"
			}).then(function (response) {
				return response.json();
			}).then((data) => {
				if (data["response"] || data["error"]) {
					this.setState({ length: 0 });
				} else {
					this.setState({ length: data["length"] });
				}
				if (data["code"] == 0) {
					this.setState({ lengthValidationColor: "red", lengthScore: 0 });
				} else if (data["code"] == 1) {
					this.setState({ lengthValidationColor: "orange", lengthScore: 0 });
				} else if (data["code"] == 2) {
					this.setState({ lengthValidationColor: "green", lengthScore: 1 });
				}
			});
		}
		checkTitle() {
			var body = [];
			body[0] = document.getElementById("id_keyword").value;
			body[1] = document.getElementById("id_title").value;
			fetch("/seo/title/", {
				method: "POST",
				credentials: 'include',
				body: JSON.stringify(body),
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
					'X-Requested-With': 'XMLHttpRequest',
					'Content-Type': 'application/json',
					'Accept': 'application/json'
				},
				dataType: "json"
			}).then(function (response) {
				return response.json();
			}).then((data) => {
				if (data["response"] == "NO_TITLE") {
					this.setState({ titleWords: 0, titleCharacters: 0 });
				} else {
					this.setState({ titleWords: data["word_count"], titleCharacters: data["character_count"] });
				}
				if (data["response"] == 'VALID_TITLE') {
					this.setState({ titleValidationColor: "green", titleScore: 1 });
				} else {
					this.setState({ titleValidationColor: "red", titleScore: 0 });
				}
			});
		}
		checkSlug() {
			var body = [];
			body[0] = document.getElementById("id_keyword").value;
			body[1] = document.getElementById("id_slug").value;
			fetch("/seo/slug/", {
				method: "POST",
				credentials: 'include',
				body: JSON.stringify(body),
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
					'X-Requested-With': 'XMLHttpRequest',
					'Content-Type': 'application/json',
					'Accept': 'application/json'
				},
				dataType: "json"
			}).then(function (response) {
				return response.json();
			}).then((data) => {
				if (data["response"] == 'VALID_SLUG') {
					this.setState({ slugValidationColor: "green", urlScore: 1 });
				} else {
					this.setState({ slugValidationColor: "red", urlScore: 0 });
				}
			});
		}
		checkInternalLinks() {
			fetch("/seo/internal_links/", {
				method: "POST",
				credentials: 'include',
				body: JSON.stringify(this.getHtml()),
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
					'X-Requested-With': 'XMLHttpRequest',
					'Content-Type': 'application/json',
					'Accept': 'application/json'
				},
				dataType: "json"
			}).then(function (response) {
				return response.json();
			}).then((data) => {
				if (data["response"] || data["error"]) {
					this.setState({ internalLinks: 0 });
				} else {
					this.setState({ internalLinks: data["internal_links"] });
				}
				if (data["code"] == 0) {
					this.setState({ internalLinksValidationColor: "red", internalLinksScore: 0 });
				} else if (data["code"] == 1) {
					this.setState({ internalLinksValidationColor: "orange", internalLinksScore: 0 });
				} else if (data["code"] == 2) {
					this.setState({ internalLinksValidationColor: "green", internalLinksScore: 1 });
				}
			});
		}
		check_h1_in_content() {
			var rich_text_blocks = document.getElementsByClassName("DraftEditor-root");
			var text;
			for (let block of rich_text_blocks) {
				text += block.innerHTML;
			}
			var raw_html_blocks = document.querySelectorAll('textarea[placeholder="RawHtml')
			for (let block of raw_html_blocks) {
				text += block.value;
			}
			fetch("/seo/title_in_article/", {
				method: "POST",
				credentials: 'include',
				body: JSON.stringify(text),
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
					'X-Requested-With': 'XMLHttpRequest',
					'Content-Type': 'application/json',
					'Accept': 'application/json'
				},
				dataType: "json"
			}).then(function (response) {
				return response.json();
			}).then((data) => {
				if (data['response'] == "H1_PRESENT") {
					this.setState({ h1_in_content_warning: "there is a h1 in your content, please remove it" });
				} else {
					this.setState({ h1_in_content_warning: "" });
				}
			});
		}
		render() {
			return [
				e('div', { class: "seo-title" },
					[
						e('img', { class: 'seo-logo', src: '/static/images/seo_logo.png', alt: "logo seo" },
							null),
						e('h2', null, "SEO results")
					]),
				e('div', { class: 'seo-toolbar' },
					e('div', null,
						[
							e('span', {
								class: `seo-indicator ${this.state.keywordValidationColor}`,
								title: this.state.keywordIndicatorTitle
							},
								this.state.keywordValidationPercentage),
							e('span',
								{ title: "The keyword must be present in the text but not too frequent (above 2% to 3% max)" },
								"Keyword repartition")
						]),
					e('div', null,
						[
							e('i',
								{ class: `icon ${this.state.lengthValidationColor}` },
								null),
							e('span',
								{ title: "The length of the article should be between 1400 and 1600 words" },
								`Length content (${this.state.length} words)`)
						]),
					e('div', null,
						[
							e('i',
								{ class: `icon ${this.state.titleValidationColor}` },
								null),
							e('span',
								{ title: "The keyword must be present in the title and title must be under 70 characters long" },
								`Title article (${this.state.titleWords} words,${this.state.titleCharacters} characters)`)
						]),
					e('div', null,
						[
							e('i',
								{ class: `icon ${this.state.slugValidationColor}` },
								null),
							e('span',
								{ title: "The keyword must be present in the slug" },
								"Url article")
						]),
					e('div', null,
						[
							e('i', { class: `icon ${this.state.internalLinksValidationColor}` },
								null),
							e('span', { title: "There must be internal links, the best is 5" },
								`Internal Links (${this.state.internalLinks} links)`)
						]),
					e('div', null,
						[
							e('span', { class: 'red' }, this.state.h1_in_content_warning)
						])
				)
			];
		}
	}
	ReactDOM.render(
		e(SeoSideBar, null, null), sidePannel);
});