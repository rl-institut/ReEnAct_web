
const colors = JSON.parse(document.getElementById("slider_colors").textContent);
const dependencies = JSON.parse(document.getElementById("slider_dependencies").textContent);


$(".js-range-slider").ionRangeSlider({
  onFinish: function (data) {
    handleSliderDependencies(data);
    update_charts('myplan-chart');
    updateColors();
  }
});


function handleSliderDependencies(data) {
  const id   = data.input.attr('id');    // e.g. "id_marsh", "id_paludiculture", "id_pv_marsh"
  const name = id.slice(3);              // remove "id_"
  const val  = data.from;                // current slider value

  // --- 1) STATIC MAX Dependencies (unchanged) ---
  if (name === "marsh") {
    Object.entries(dependencies.areas_at_full_marsh_usage).forEach(([target, area]) => {
      const ratio = area / dependencies.marsh_max_area;
      const newMax = Math.round(val * ratio * dependencies.densities[target]);
      $('#id_' + target)
        .data('ionRangeSlider')
        .update({ max: newMax });
    });
  }

  // --- 2) COMPETITION: adjust only 'from', not max ---
  // sum of areas (ha) for paludiculture & pv_marsh ≤ marsh * sum_ratio
  if (name === 'paludiculture' || name === 'pv_marsh') {
    const marshVal = $('#id_marsh').data('ionRangeSlider').result.from;
    const capHa    = marshVal * dependencies.areas_at_full_marsh_usage.paludiculture / dependencies.marsh_max_area;

    if (name === 'paludiculture') {
      // user moved paludiculture → compute allowed pv_marsh area
      const paluTM   = val;
      const paluHa   = paluTM / dependencies.densities.paludiculture;
      let allowedPvHa = capHa - paluHa;
      if (allowedPvHa < 0) allowedPvHa = 0;
      const allowedPvMW = allowedPvHa * dependencies.densities.pv_marsh;

      const pvSlider   = $('#id_pv_marsh').data('ionRangeSlider');
      const currentPv  = pvSlider.result.from;  // in ha

      // only update if current Pv > allowedPv
      if (currentPv > allowedPvMW) {
        pvSlider.update({ from: allowedPvMW });
      }
    }
    else { // name === 'pv_marsh'
      // user moved pv_marsh → compute allowed paludiculture TM
      const pvMW = val;
      const pvHa = pvMW / dependencies.densities.pv_marsh;
      let allowedPaluHa = capHa - pvHa;
      if (allowedPaluHa < 0) allowedPaluHa = 0;
      const allowedPaluTM = Math.round(allowedPaluHa * dependencies.densities.paludiculture);

      const paluSlider  = $('#id_paludiculture').data('ionRangeSlider');
      const currentPalu = paluSlider.result.from; // in TM

      // only update if current Palu TM > allowed Palu TM
      if (currentPalu > allowedPaluTM) {
        paluSlider.update({ from: allowedPaluTM });
      }
    }
  }
}

// updateSliderMarks();
updateColors();

// Update the colors of the sliders based on the color scheme and the contrast ratio with white text
function getLuminance(rgb) {
  const [r, g, b] = rgb.map(c => {
    c /= 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
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

$(document).ready(function() {
  const marshSlider = $("#id_marsh").data("ionRangeSlider");
  handleSliderDependencies({
    input: $("#id_marsh"),
    from:  marshSlider.result.from
  });
  updateColors();
});
