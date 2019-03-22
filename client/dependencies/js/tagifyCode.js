// let input = document.querySelector('input[name=emailTags]'),
//     // init Tagify script on the above inputs
//     tagify = new Tagify(input, {
//         blacklist : [".NET", "PHP"] // <-- passed as an attribute in this demo
//     });

// // Chainable event listeners
// tagify.on('add', onAddTag)
//       .on('remove', onRemoveTag)
//       .on('input', onInput)
//       .on('edit', onTagEdit)
//       .on('invalid', onInvalidTag)
//       .on('click', onTagClick);

// // tag added callback
// function onAddTag(e){
//     console.log("onAddTag: ", e.detail);
//     console.log("original input value: ", input.value)
//     tagify.off('add', onAddTag) // exmaple of removing a custom Tagify event
// }

// // tag remvoed callback
// function onRemoveTag(e){
//     console.log(e.detail);
//     console.log("tagify instance value:", tagify.value)
// }

// // on character(s) added/removed (user is typing/deleting)
// function onInput(e){
//     console.log(e.detail);
//     console.log("onInput: ", e.detail);
// }

// function onTagEdit(e){
//     console.log("onTagEdit: ", e.detail);
// }

// // invalid tag added callback
// function onInvalidTag(e){
//     console.log("onInvalidTag: ", e.detail);
// }

// // invalid tag added callback
// function onTagClick(e){
//     console.log(e.detail);
//     console.log("onTagClick: ", e.detail);
// }