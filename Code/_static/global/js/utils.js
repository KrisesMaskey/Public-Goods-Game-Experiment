// Validates Input to enable next button
function inputValidator(args, submit){
    let flag = false;
    let keyList = Object.keys(args);
    let inputs = [];

    for(const key of keyList){
        if(key === 'checked'){
            const checkedInputs = document.querySelectorAll('.question input:checked');
            if(checkedInputs.length === args[key]){
                flag = true;
                if(submit) checkedInputs.forEach((item)=>{inputs.push(item.value)});
                continue;
            }
            else{
                flag = false;
                break;
            }
        }
        else if(key === 'range'){
            const rangeInputs = document.querySelectorAll('input[type="range"]');
            const rangeWithValue = Array.from(rangeInputs).filter(input => input.classList.contains('active'));
            if(rangeWithValue.length === args[key]){
                flag = true;
                if(submit) rangeWithValue.forEach((item)=>{inputs.push(item.value)});
                continue;
            }
            else{
                flag = false;
                break;
            }
        }
        else if(key === 'text'){
            const textInputs = document.querySelectorAll('input[type="text"]:not(:placeholder-shown)');
            if(textInputs.length === args[key]){
                flag = true;
                if(submit) textInputs.forEach((item)=>{inputs.push(item.value)});
                continue;
            }
            else{
                flag = false;
                break;
            }
        }
        else if(key === 'select'){
            const selectInputs = document.querySelectorAll('select');
            const selectWithValue = Array.from(selectInputs).filter(select => select.value !== "");
            if(selectWithValue.length === args[key]){
                flag = true;
                if(submit) selectWithValue.forEach((item)=>{inputs.push(item.value)});
                continue;
            }
            else{
                flag = false;
                break;
            }
        }
        else if(key === 'text-area'){
            const textAreaInputs = document.querySelectorAll('textarea:not(:placeholder-shown)');
            if(textAreaInputs.length === args[key]){
                flag = true;
                if(submit) textAreaInputs.forEach((item)=>{inputs.push(item.value)});
                continue;
            }
            else{
                flag = false;
                break;
            }
        }
    }

    return submit === true ? inputs : flag;    
}

// Form Handler
function checkFormValidity(event, page, submit = false, args = null){
    let nextButton = null;

    switch (String(page)) {
        case 'mturk-id':
            const input_value = document.getElementById('mturk_id').value.trim();
            if (input_value === "") {
                event.preventDefault();
                alert("MTurk ID cannot be blank!");
            } 
            else {
                liveSend({ "type": "mturk-id", "id": input_value });
            }
            break;
        
        case 'preliminary-questions':
            const submitBtn = document.getElementById('submitBtn');
            const ageInput = document.getElementById('age').value.trim();
            const genderInput = document.querySelector('input[name="gender"]:checked');
            const groupInput = document.querySelectorAll('input[name="group"]:checked');
            const locationInput = document.getElementById('location').value;
            enableFlag = true;

            if(!ageInput) enableFlag = false;
            if(!genderInput) enableFlag = false;
            if(groupInput.length < 1) enableFlag = false;
            if(!locationInput) enableFlag = false;
            submitBtn.disabled = !enableFlag;   

            if(submit){
                if(!/^\d+$/.test(ageInput) || parseInt(ageInput) < 1 || parseInt(ageInput) > 95){
                    event.preventDefault();
                    alert('Please enter a valid age (numbers only)');
                }
                else{
                    race = [];
                    groupInput.forEach((item)=>{race.push(item.value)});
                    liveSend({ "type":"preliminary-questions", "age": parseInt(ageInput), "gender": genderInput.value, "race": JSON.stringify(race), "location":locationInput})
                }
            }
            break;

        case 'quiz-submit':
            nextButton = document.getElementById('quizButton');
            nextButton.disabled = submit ? false : !inputValidator(args, submit);

            if(submit){
                event.preventDefault();
                inputs = Array.from(inputValidator(args, true));
                liveSend({"type": "quiz-submit", "answers": JSON.stringify(inputs)});
            }
            break;

        case 'post-experiment-questions':
            nextButton = document.getElementById('next-button');
            nextButton.disabled = submit ? false : !inputValidator(args, submit);

            if(submit){
                inputs = Array.from(inputValidator(args, true));
                liveSend({"type": "peq", "inputs": inputs});
            }
            break;
        
        case 'game-interface':
            nextButton = document.getElementById('next-button');
            nextButton.disabled = submit ? false : !inputValidator(args, submit);

            if(submit){
                inputs = Array.from(inputValidator(args, true));
                liveSend({"type": "game-page", "inputs": inputs});
            }
            break;

        default:
            console.log("Unknown page type");
    }
}

// Receive data from backend
function liveRecv(value) {
    if (value.type === 'quiz-result') {
        if (value.response){
            document.getElementById("invisibleButton").click();
        }
        else{
            if(value.cnt == 1){
                move(event, 1);
            }

            else if(value.cnt > 1){
                document.getElementById("invisibleButton").click();
            }
        }
    }
    else if(value.type === 'next-page'){
        document.getElementById("invisibleButton").click();
    } 
    else if(value.type === 'contribution-submitted'){
        progress_cnter = parseInt(value.progress);
        const progressBars = document.querySelectorAll('.p-bar');
        progressBars.forEach((bar, index) => {
            if (index < progress_cnter) {
                bar.style.backgroundColor = 'green';
            } else {
                bar.style.backgroundColor = 'white';
            }
        });
    }
}

// Move Tabs in Instruction Page
function move(e, n) {
    e.preventDefault();
    let tabs = document.getElementById('navbar').children;
    let contents = document.getElementsByClassName('tab-content');
    // Remove the 'active' class from the current tab content
    contents[index].classList.remove('active');
    index += n;
    if (index >= tabs.length) {
        index = 0;
    } else if (index < 0) {
        index = tabs.length - 1;
    }
    let tab = tabs[index].children[0];
    window.location.hash = tab.getAttribute('href');
    // Add the 'active' class to the new tab content
    contents[index].classList.add('active');
}