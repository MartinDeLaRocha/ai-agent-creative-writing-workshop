package com.example.kosmosconverter

import android.app.DatePickerDialog
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import java.time.LocalDate
import java.time.ZoneOffset

class MainActivity : AppCompatActivity() {
    private lateinit var birthLabel: TextView
    private lateinit var interestLabel: TextView
    private lateinit var results: TextView
    private var birth: LocalDate = LocalDate.now(ZoneOffset.UTC).minusYears(30)
    private var interest: LocalDate = LocalDate.now(ZoneOffset.UTC)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        birthLabel = findViewById(R.id.birthLabel)
        interestLabel = findViewById(R.id.interestLabel)
        results = findViewById(R.id.results)

        // Prepopulate: birth defaults to 30 years before today; interest = TODAY.
        render()

        findViewById<Button>(R.id.pickBirth).setOnClickListener {
            pickDate(birth) { birth = it; render() }
        }
        findViewById<Button>(R.id.pickInterest).setOnClickListener {
            pickDate(interest) { interest = it; render() }
        }
        findViewById<Button>(R.id.todayButton).setOnClickListener {
            interest = LocalDate.now(ZoneOffset.UTC); render()
        }
        findViewById<Button>(R.id.convertButton).setOnClickListener { convert() }
    }

    private fun pickDate(initial: LocalDate, onPicked: (LocalDate) -> Unit) {
        DatePickerDialog(
            this,
            { _, y, m, d -> onPicked(LocalDate.of(y, m + 1, d)) },
            initial.year, initial.monthValue - 1, initial.dayOfMonth,
        ).show()
    }

    private fun render() {
        birthLabel.text = "Birth date: $birth"
        interestLabel.text = "Date of interest: $interest"
    }

    private fun convert() {
        try {
            val r = KosmosConverter.convert(birth, interest)
            results.text = buildString {
                append("Birth:  ${r.birth}\n")
                append("Date:   ${r.interest}\n\n")
                append("Interval: ${r.intervalDays} days\n")
                append("Periods: ${r.periods}\n\n")
                append(r.note)
            }
        } catch (e: IllegalArgumentException) {
            results.text = e.message
        }
    }
}
