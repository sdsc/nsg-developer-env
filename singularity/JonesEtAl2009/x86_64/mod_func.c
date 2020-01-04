#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _ar_reg(void);
extern void _ca_reg(void);
extern void _cad_reg(void);
extern void _cat_reg(void);
extern void _dipole_reg(void);
extern void _kca_reg(void);
extern void _km_reg(void);
extern void _pp_dipole_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," mod_files/ar.mod");
    fprintf(stderr," mod_files/ca.mod");
    fprintf(stderr," mod_files/cad.mod");
    fprintf(stderr," mod_files/cat.mod");
    fprintf(stderr," mod_files/dipole.mod");
    fprintf(stderr," mod_files/kca.mod");
    fprintf(stderr," mod_files/km.mod");
    fprintf(stderr," mod_files/pp_dipole.mod");
    fprintf(stderr, "\n");
  }
  _ar_reg();
  _ca_reg();
  _cad_reg();
  _cat_reg();
  _dipole_reg();
  _kca_reg();
  _km_reg();
  _pp_dipole_reg();
}
