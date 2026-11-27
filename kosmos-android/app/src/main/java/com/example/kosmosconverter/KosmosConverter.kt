package com.example.kosmosconverter

import java.time.LocalDate

/**
 * Kosmos-1 Y2K date converter.
 * Cycles: 23, 28, 33 days -> common period 21,252 days.
 * Both dates are shifted backward by whole periods until both are in 1901-1999,
 * preserving the elapsed interval and the weekday of each date.
 */
object KosmosConverter {
    const val PERIOD_DAYS: Long = 23L * 28L * 33L

    data class Result(
        val birth: String,
        val interest: String,
        val intervalDays: Long,
        val periods: Int,
        val note: String,
    )

    fun convert(birth: LocalDate, interest: LocalDate): Result {
        require(!interest.isBefore(birth)) {
            "The date of interest must be on or after the birth date."
        }
        var cb = birth
        var ci = interest
        var periods = 0
        while (ci.year > 1999 || cb.year > 1999) {
            cb = cb.minusDays(PERIOD_DAYS)
            ci = ci.minusDays(PERIOD_DAYS)
            periods++
        }
        require(cb.year in 1901..1999 && ci.year in 1901..1999) {
            "These dates cannot both be represented in 1901-1999."
        }
        val note = if (periods == 0) {
            "Both dates are already within 1901-1999. No shift was necessary."
        } else {
            val plural = if (periods == 1) "period" else "periods"
            "Both dates shifted back by ${String.format("%,d", periods * PERIOD_DAYS)} days " +
                "($periods complete $plural). Interval and weekday are preserved."
        }
        return Result(
            birth = fmt(cb), interest = fmt(ci),
            intervalDays = java.time.temporal.ChronoUnit.DAYS.between(birth, interest),
            periods = periods, note = note,
        )
    }

    private fun fmt(d: LocalDate): String =
        "%02d %02d %02d".format(d.monthValue, d.dayOfMonth, d.year % 100)
}
