from BatteryLUTS import *


class Battery:
    """
        Usage:
            - Periodically call Update(voltage,current,temperature,timestamp) in SI units.
            - Access current State-of-charge estimate by referencing instance.SOC
    """
    Vt = 0
    I = 0
    T = 0
    t_elapsed = 0

    P_GAIN = 10
    I_GAIN = .01
    HYST_GAIN = 17.45
    SHORT_TERM_DAMP = 2
    SOC_CORRECTION_INTERVAL = 30

    def __init__(self, SOC_init, timestamp, P_GAIN=10, I_GAIN=.01, HYST_GAIN=17.45, CORRECTION_INTERVAL=30):
        # Assumes 0 current on startup
        self.SOCVoc = SOC_init
        self.SOC = SOC_init
        self.t = timestamp
        self.P_GAIN = P_GAIN
        self.I_GAIN = I_GAIN
        self.HYST_GAIN = HYST_GAIN
        self.SOC_CORRECTION_INTERVAL = CORRECTION_INTERVAL
        self.t_elapsed_long = 0
        # state vars for MeasureVoc
        self.V1 = 0
        self.V2 = 0
        # State Vars for UpdateSOCCC
        self.SOCCC = SOC_init
        # State Vars for EstimateVoc
        self.Hyst = 0
        # State vars for PI
        self.Voc_error_integral = 0

    def update(self, Vt, I, T, timestamp):
        # Assign new params ###############
        self.Vt = Vt
        self.I = I
        self.T = T
        self.t_elapsed = timestamp - self.t
        self.t = timestamp
        # print "elapsed:" + str(self.t_elapsed)
        # Calculate Voc true and estimate
        self._measure_voc()
        self._estimate_voc()
        # print "voctrue:" + str(self.Voc)
        # print "vocest:" + str(self.VocSOC)
        # calculate SOC using two methods
        self._updateSOCCC()
        self._updateSOCVoc()

        # Final SOC estimate is VOCCC periodically corrected towards SOCVoc
        self.t_elapsed_long += self.t_elapsed
        self.SOC = self.SOCCC
        if self.t_elapsed_long > self.SOC_CORRECTION_INTERVAL:
            self.t_elapsed_long = 0
            self.SOCCC += (self.SOCVoc - self.SOCCC) / 2
        # print "SOCV=" + str(round(self.SOCVoc)) + ";" + "SOCC=" + str(round(self.SOCCC))
        return self.SOC

    def _measure_voc(self):
        """
            Calculates the 'true' Voc using the input measurements and RC circuit dynamics
        :return:
        """
        # Update Circuit Parameters
        self.C1 = C1_lut[self.SOCVoc]
        self.C2 = C2_lut[self.SOCVoc]
        self.R0 = R0_lut[self.SOCVoc]
        self.R1 = R1_lut[self.SOCVoc]
        self.R2 = R2_lut[self.SOCVoc]
        #  Update V0
        self.V0 = self.R0 * self.I / 1000
        #  Update V1
        V1_prime_now = ((self.I / self.C1) - (self.V1 / (self.C1 * self.SHORT_TERM_DAMP * self.R1)))
        self.V1 += V1_prime_now * self.t_elapsed
        # print "v1:" + str(self.V1)
        #  Update V2
        V2_prime_now = ((self.I / self.C2) - (self.V2 / (self.C2 * self.R2)))
        self.V2 += V2_prime_now * self.t_elapsed
        # print "v2:" + str(self.V2)
        #  Update Voc estimate
        self.Voc = self.Vt + self.V0 + self.V1 + self.V2

    # self.Voc = self.Vt + self.V0
    def _estimate_voc(self):
        """
            Calculates the estimated Voc using SOC
        :return:
        """
        #  Get Voc estimate via previously estimated SOC
        self.Capacity = Capacity_lut[abs(self.I)]
        OCVCharge = OCVCharge_lut[self.SOCVoc]
        OCVDischarge = OCVDischarge_lut[self.SOCVoc]
        Hyst1 = abs(self.I) * self.HYST_GAIN / self.Capacity
        Hyst2 = (OCVDischarge - OCVCharge) * Hyst1 / 2
        self.Hyst += (Hyst2 - Hyst1 * self.Hyst) * self.t_elapsed
        tempcorr = tempcorr_lut[self.SOCVoc] * (self.T - 23)
        self.VocSOC = (OCVDischarge + OCVCharge) / 2 + self.Hyst + tempcorr

    def _updateSOCCC(self):
        """
            Calculates SOC using Coulomb Counting
        :return:
        """
        #  Update SOC estimate by Coulomb Counting
        self.Capacity = Capacity_lut[abs(self.I)]
        self.SOCCC -= 100 * (self.I / self.Capacity) * self.t_elapsed

    def _updateSOCVoc(self):
        """
            Calculates SOC using a PI observer
        :return:
        """
        # use PI observer to get SOC using Voc
        Voc_error = self.Voc - self.VocSOC
        self.Voc_error_integral += self.t_elapsed * Voc_error
        # self.SOCVoc = SOCVoc_lut[self.VocSOC]
        self.SOCVoc += self.P_GAIN * Voc_error + self.I_GAIN * self.Voc_error_integral
