var similar_cases = null;

async function query(query_text) {
    response = await fetch('/query?query='+encodeURIComponent(query_text));
    similar_cases = JSON.parse(await response.text());
}

function append_results_title() {
    var results_title = document.createElement('h3');
    results_title.innerText = 'Zusammenfassungen der Präzedenzfälle:';
    var similar_cases = document.querySelector('#similar-cases');
    similar_cases.appendChild(results_title);
}

function close_case_modal() {
    var case_modal_wrapper = document.querySelector('#case-modal-wrapper');
    case_modal_wrapper.remove();
}

function open_case_modal(idx) {
    var case_modal_wrapper = document.createElement('div');
    case_modal_wrapper.id = 'case-modal-wrapper';

    var case_modal = document.createElement('div');
    case_modal.id = 'case-modal';
    case_modal.innerText = similar_cases.documents[idx]
    case_modal_wrapper.appendChild(case_modal);

    var close_case_button = document.createElement('div');
    close_case_button.id = 'close-case-button';
    close_case_button.innerText = 'x'
    close_case_button.onclick = close_case_modal
    case_modal.appendChild(close_case_button)

    var body = document.querySelector('body');
    body.appendChild(case_modal_wrapper);
}

function append_case_card(idx, summary) {
    var case_card = document.createElement('div');
    case_card.className = 'case-card';
    case_card.id = 'case-' + idx;
    case_card.innerText = summary;

    var open_case_button = document.createElement('div');
    open_case_button.className = 'open-case-button';
    open_case_button.innerText = 'Fall ansehen';
    open_case_button.onclick = () => open_case_modal(idx)
    case_card.appendChild(open_case_button)

    var similar_cases = document.querySelector('#similar-cases');
    similar_cases.appendChild(case_card);
}

function append_progress_bar() {
    var progress_bar_wrapper = document.createElement('div');
    progress_bar_wrapper.id = 'progress-bar-wrapper'
    progress_bar_wrapper.innerText = 'Die Anfrage ist in Bearbeitung... Bitte warten.'

    var progress_bar = document.createElement('div');
    progress_bar.id = 'progress-bar';
    progress_bar_wrapper.appendChild(progress_bar)
    
    var progress_color = document.createElement('div');
    progress_color.id = 'progress-color';
    progress_bar.appendChild(progress_color);

    var similar_cases = document.querySelector('#similar-cases');
    similar_cases.appendChild(progress_bar_wrapper);
}

function remove_progress_bar() {
    var loading = document.querySelector('#progress-bar-wrapper');
    loading.remove();
}

function clear_results() {
    var similar_cases = document.querySelector('#similar-cases');
    similar_cases.innerHTML = '';
}

async function on_submit() {
    var query_text = document.querySelector('#user-case-text')?.value;
    if (query_text == '') return
    clear_results();
    append_results_title();
    append_progress_bar();
    await query(query_text);
    remove_progress_bar();
    for (var i in similar_cases.summaries) {
        append_case_card(i, similar_cases.summaries[i])
    }
}

function initialize() {
    var submit_button = document.querySelector('#user-case-submit');
    submit_button.addEventListener('click', on_submit);
}

document.addEventListener('DOMContentLoaded', initialize);