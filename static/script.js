var similar_cases = null;

async function query(query_text) {
    response = await fetch('/query?query='+encodeURIComponent(query_text));
    similar_cases = JSON.parse(await response.text());
    console.log('Completed: query')
}

function append_results_title() {
    var results_title = document.createElement('h3');
    results_title.innerText = 'Results:';
    var similar_cases = document.querySelector('#similar-cases');
    similar_cases.appendChild(results_title);
    console.log('Completed: append_results_title')
}

function append_case_card(id, summary) {
    var case_card = document.createElement('div');
    case_card.className = 'case-card';
    case_card.id = id;
    case_card.innerText = summary;

    var similar_cases = document.querySelector('#similar-cases');
    similar_cases.appendChild(case_card);
    console.log('Completed: append_case_card')
}

async function on_submit() {
    var query_text = document.querySelector('#user-case-text')?.value;
    if (query_text == '') return
    await query(query_text);
    append_results_title();
    for (var i in similar_cases.summaries) {
        append_case_card(i, similar_cases.summaries[i])
    }
    console.log('Completed: on_submit')
}

function initialize() {
    var submit_button = document.querySelector('#user-case-submit');
    submit_button.addEventListener('click', on_submit);
    console.log('Completed: initialize')
}

document.addEventListener('DOMContentLoaded', initialize);