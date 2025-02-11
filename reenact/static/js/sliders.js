
$(".js-range-slider").ionRangeSlider();
// updateSliderMarks();

function convertToPercent(num, min, max) {
  return ((num - min) / (max - min)) * 100;
}

function addMarks(data, marks) {
  let html = "";
  for (let i = 0; i < marks.length; i++) {
    let percent = convertToPercent(marks[i][1], data.min, data.max);
    // Fix percentage due to offset
    percent = percent - 2.5 - (3.5 * percent) / 100;
    html += `<span class="showcase__mark" style="left: ${percent}%">`;
    html += marks[i][0];
    html += "</span>";
  }
  data.slider.append(html);
}

function updateSliderMarks(msg) {
  const sliderMarks = JSON.parse(document.getElementById('slider_marks').textContent);
  for (let [slider_name, slider_marks] of sliderMarks) {
    let slider = $(`#id_${slider_name}`).data("ionRangeSlider");
    slider.update({
      // jshint ignore:start
      onUpdate: function (data) {
        addMarks(data, slider_marks);
      },
      // jshint ignore:end
    });
  }
}
