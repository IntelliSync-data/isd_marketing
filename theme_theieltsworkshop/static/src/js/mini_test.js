/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

const sampleQuestions = [
    {
        id: 1,
        question: "Complete the sentence: If I _______ more time, I would have joined the advanced IELTS course.",
        options: ["had", "had had", "have had", "would have"],
        correct: 1,
        explanation: "Câu điều kiện loại 3 (Third Conditional) diễn tả giả định trái ngược với quá khứ: If + had + V3/ed, S + would have + V3/ed.",
    },
    {
        id: 2,
        question: "Choose the synonym for 'ubiquitous' in academic writing:",
        options: ["omnipresent", "scarce", "insignificant", "temporary"],
        correct: 0,
        explanation: "'Ubiquitous' mang nghĩa xuất hiện khắp nơi, đồng nghĩa với 'omnipresent' hay 'widespread'.",
    },
    {
        id: 3,
        question: "In IELTS Writing Task 1, which phrase is best to describe a dramatic increase?",
        options: ["decreased steadily", "soared substantially", "fluctuated wildly", "leveled off"],
        correct: 1,
        explanation: "'Soared substantially' dùng để miêu tả sự tăng vọt, tăng mạnh và nhanh.",
    },
    {
        id: 4,
        question: "Identify the correct collocation for academic achievement:",
        options: ["make success", "achieve success", "do success", "take success"],
        correct: 1,
        explanation: "Collocation tự nhiên và chuẩn xác trong tiếng Anh là 'achieve success'.",
    },
];

publicWidget.registry.TiwMiniTest = publicWidget.Widget.extend({
    selector: '.s_tiw_mini_test',
    events: {
        'click .option-btn': '_onSelectOption',
        'click .btn-next-question': '_onNextQuestion',
        'click .btn-prev-question': '_onPrevQuestion',
        'click .btn-restart-test': '_onRestartTest',
    },

    start: function () {
        this.currentQ = 0;
        this.selectedAnswers = {};
        this._renderQuestion();
        return this._super.apply(this, arguments);
    },

    _renderQuestion: function () {
        const q = sampleQuestions[this.currentQ];
        const total = sampleQuestions.length;
        const progressPercent = Math.round(((this.currentQ + 1) / total) * 100);

        const $stepIndicator = this.$('.mini-test-step');
        const $progressBar = this.$('.mini-test-progress');
        const $questionText = this.$('.mini-test-question-text');
        const $optionsContainer = this.$('.mini-test-options');
        const $btnPrev = this.$('.btn-prev-question');
        const $btnNext = this.$('.btn-next-question');

        if ($stepIndicator.length) {
            $stepIndicator.text(`Câu hỏi ${this.currentQ + 1} / ${total}`);
        }
        if ($progressBar.length) {
            $progressBar.css('width', `${progressPercent}%`);
        }
        if ($questionText.length) {
            $questionText.text(q.question);
        }

        if ($optionsContainer.length) {
            let html = '';
            q.options.forEach((opt, idx) => {
                const char = String.fromCharCode(65 + idx);
                const isSelected = this.selectedAnswers[this.currentQ] === idx;
                html += `
                    <button type="button" class="option-btn ${isSelected ? 'selected' : ''}" data-idx="${idx}">
                        <span><strong class="me-2">${char}.</strong>${opt}</span>
                        ${isSelected ? '<i class="fa fa-check-circle text-warning fs-5"></i>' : ''}
                    </button>
                `;
            });
            $optionsContainer.html(html);
        }

        if ($btnPrev.length) {
            $btnPrev.prop('disabled', this.currentQ === 0);
        }
        if ($btnNext.length) {
            const hasAnswer = this.selectedAnswers[this.currentQ] !== undefined;
            $btnNext.prop('disabled', !hasAnswer);
            $btnNext.text(this.currentQ === total - 1 ? 'Xem Kết Quả' : 'Câu Tiếp Theo');
        }
    },

    _onSelectOption: function (ev) {
        const optionIdx = parseInt($(ev.currentTarget).data('idx'), 10);
        this.selectedAnswers[this.currentQ] = optionIdx;
        this._renderQuestion();
    },

    _onNextQuestion: function () {
        if (this.currentQ < sampleQuestions.length - 1) {
            this.currentQ++;
            this._renderQuestion();
        } else {
            this._showResults();
        }
    },

    _onPrevQuestion: function () {
        if (this.currentQ > 0) {
            this.currentQ--;
            this._renderQuestion();
        }
    },

    _showResults: function () {
        let score = 0;
        for (let i = 0; i < sampleQuestions.length; i++) {
            if (this.selectedAnswers[i] === sampleQuestions[i].correct) {
                score++;
            }
        }

        let bandText = "Band 3.5 - 4.5 (Cần củng cố nền tảng)";
        if (score === 4) bandText = "Band 7.0 - 8.0 (Nâng cao)";
        else if (score === 3) bandText = "Band 6.0 - 6.5 (Khá)";
        else if (score === 2) bandText = "Band 5.0 - 5.5 (Trung bình)";

        this.$('.mini-test-active-view').addClass('d-none');
        this.$('.mini-test-result-view').removeClass('d-none');
        this.$('.result-score').text(`${score}/${sampleQuestions.length}`);
        this.$('.result-band').text(bandText);
    },

    _onRestartTest: function () {
        this.currentQ = 0;
        this.selectedAnswers = {};
        this.$('.mini-test-result-view').addClass('d-none');
        this.$('.mini-test-active-view').removeClass('d-none');
        this._renderQuestion();
    },
});

export default publicWidget.registry.TiwMiniTest;

