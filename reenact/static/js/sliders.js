
const colors = JSON.parse(document.getElementById("slider_colors").textContent);


$(".js-range-slider").ionRangeSlider({
  onFinish: function (data) {
    update_charts('myplan-chart');
  }
});

// updateSliderMarks();
updateColors();

// Update the colors of the sliders based on the color scheme and the contrast ratio with white text
function getLuminance(rgb) {
  const [r, g, b] = rgb.map(c => {
    c /= 255;
    return c <= 0.03928
      ? c / 12.92
      : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contrastRatio(rgb1, rgb2) {
  const lum1 = getLuminance(rgb1);
  const lum2 = getLuminance(rgb2);
  const brightest = Math.max(lum1, lum2);
  const darkest = Math.min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05);
}

function hexToRgb(hex) {
  const bigint = parseInt(hex.slice(1), 16);
  return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255];
}

function updateColors() {
  document.getElementById("capacityForm").querySelectorAll("input").forEach(function(item) {
    const sliderColor = colors[item.id.slice(3)];
    if (sliderColor !== undefined) {
      const rgb = hexToRgb(sliderColor);
      const white = [255, 255, 255];
      const textColor = contrastRatio(rgb, white) >= 4.5 ? "#ffffff" : "#000000";

      item.parentElement.querySelector(".irs-bar").style.backgroundColor = sliderColor;
      const irsSingle = item.parentElement.querySelector(".irs-single");
      irsSingle.style.backgroundColor = sliderColor;
      irsSingle.style.color = textColor;
    }
  });
}

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
